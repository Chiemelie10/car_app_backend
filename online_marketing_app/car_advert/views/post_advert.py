"""This module defines class PostAdvert."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_advert.utils import validate_mimetype
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from image.models import Image
from user_activity.models import UserActivity


class PostAdvert(APIView):
    """This class creates a new car advert in the database."""
    # pylint: disable=no-member

    permission_classes = [IsAdminUser]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def validate_images(self, validated_data):
        """This method validates images."""
        uploaded_images = validated_data.get('uploaded_images', None)
        uploaded_cloud_images = validated_data.get('uploaded_cloud_images', None)

        if uploaded_images and uploaded_cloud_images:
            raise ValueError('You can either save images '\
                             'to the cloud or server, but not both.')

        if not uploaded_images and not uploaded_cloud_images:
            raise ValueError('Images are required.')

        if uploaded_images and len(uploaded_images) < 5:
            raise ValueError('Uploaded images cannot be less than 5.')

        if uploaded_images and len(uploaded_images) > 10:
            raise ValueError('Uploaded images cannot be more than 10.')

        if uploaded_cloud_images and len(uploaded_cloud_images) < 5:
            raise ValueError('Uploaded images cannot be less than 5.')

        if uploaded_cloud_images and len(uploaded_cloud_images) > 10:
            raise ValueError('Uploaded images cannot be more than 10.')

        if uploaded_cloud_images:
            validated_data['is_cloud_server_images'] = True

    def validate_thumbnail(self, validated_data):
        """This method validates thumbnail"""
        thumbnail = validated_data.get('thumbnail', None)

        if thumbnail:
            validate_mimetype(thumbnail)

        thumbnail_cloud = validated_data.get('thumbnail_cloud', None)

        if thumbnail and thumbnail_cloud:
            raise ValueError('You can either save images '\
                             'to the cloud or server, but not both.')

        if not thumbnail and not thumbnail_cloud:
            raise ValueError('Thumbnail is required.')

        if thumbnail_cloud:
            validated_data['is_cloud_server_thumbnail'] = True

    def validate_state_city(self, validated_data):
        """This method enforces state and city foreign key relationship"""
        city = validated_data.get('city')
        state = validated_data.get('state')
        cities = state.cities.all()
        if city not in cities:
            raise ValueError('Provided city must have a matching state.')

    def validate_brand_model(self, validated_data):
        """This method enforces brand and model foreign key relationship."""
        model = validated_data.get('model')
        brand = validated_data.get('brand')
        brand_models = brand.brand_models.all()
        if model not in brand_models:
            raise ValueError('Provided car model must have a matching car brand.')

    def generate_tag_values(self, validated_data):
        """
        This method generates values for the tag column of each instance
        of the car_adverts table.
        """
        year = validated_data.get('year').year
        fuel_type = validated_data.get('fuel_type')
        city = validated_data.get('city')
        state = validated_data.get('state')
        model = validated_data.get('model')
        brand = validated_data.get('brand')
        user = validated_data.get('user')

        validated_data['tag'] = f'{year}, {brand.name}, {model.name}, {fuel_type}, '\
                                f'{state.name}, {city.name}, {user.username}'

    def save_multiple_server_images(self, uploaded_images, image_model, car_advert_instance):
        """
        This function saves multiple images with a foreign key
        relationship to an advert instance to the server and database.
        """
        for image in uploaded_images:
            try:
                validate_mimetype(image)
                image_model.objects.create(car_advert=car_advert_instance, image=image)
            except Exception as error: # pylint: disable=broad-exception-caught
                car_advert_instance.delete()
                return JsonResponse({'error': str(error)}, status=400)

    def save_multiple_cloud_images(self, uploaded_cloud_images, image_model, car_advert_instance):
        """
        This function saves multiple cloud images with a foreign key
        relationship to an advert instance to the database.
        """
        for image in uploaded_cloud_images:
            try:
                image_model.objects.create(car_advert=car_advert_instance, cloud_image=image)
            except Exception as error: # pylint: disable=broad-exception-caught
                car_advert_instance.delete()
                return JsonResponse({'error': str(error)}, status=400)

    def post(self, request):
        """
        This method validates a post request from api/create-advert route
        and saves it to the database if successful.
        """
        serializer = CarAdvertSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            try:
                self.validate_images(validated_data)
                self.validate_thumbnail(validated_data)
                self.validate_brand_model(validated_data)
                self.validate_state_city(validated_data)
            except Exception as error_message: # pylint: disable=broad-exception-caught
                return JsonResponse({'error': str(error_message)}, status=400)

            result = decode_token(request)

            if isinstance(result, JsonResponse):
                return result

            user = validated_data.get('user')
            if not user:
                return JsonResponse({'error': 'User is required.'}, status=400)

            user_id, is_superuser, _ = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == user.id:
                uploaded_images = validated_data.pop('uploaded_images', None)
                uploaded_cloud_images = validated_data.pop('uploaded_cloud_images', None)
                self.generate_tag_values(validated_data)

                car_advert = CarAdvert(**validated_data)
                car_advert.save()

                if uploaded_images:
                    upload_error = self.save_multiple_server_images(uploaded_images, Image,
                                                                    car_advert)
                    if upload_error:
                        return upload_error
                elif uploaded_cloud_images:
                    upload_error = self.save_multiple_cloud_images(uploaded_cloud_images, Image,
                                                              car_advert)
                    if upload_error:
                        return upload_error

                if is_superuser is True:
                    try:
                        action_performing_user = User.objects.get(id=user_id)
                    except User.DoesNotExist:
                        return JsonResponse({'error': 'Provided token has no valid user.'}, 401)
                elif user_manager is True:
                    action_performing_user = manager
                else:
                    action_performing_user = user

                UserActivity.objects.create(
                    user = action_performing_user,
                    activity_type = 'Create',
                    activity_details = f'Advert owner: {user.id} '\
                                        f'\nAdvert ID: {car_advert.id}',
                )

                serializer = CarAdvertSerializer(car_advert)
                return JsonResponse(serializer.data, status=201)

            if user_manager is False or manager is None:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        return JsonResponse(serializer.errors, status=400)
