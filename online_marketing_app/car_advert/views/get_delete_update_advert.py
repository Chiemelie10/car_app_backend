"""This module defines class GetDeleteUpdateAdvert."""
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_advert.utils import validate_mimetype
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from image.models import Image
from user_activity.models import UserActivity


class GetDeleteUpdateAdvert(APIView):
    """
    This class defines methods to get, delete or update single
    car advert request.data in the database.
    """
    # pylint: disable=unused-argument
    # pylint: disable=no-member
    # pylint: disable=invalid-name

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def validate_state_city(self, validated_data, car_advert_instance):
        """This method enforces state and city foreign key relationship."""
        if 'city' in validated_data and 'state' in validated_data:
            city = validated_data['city']
            state = validated_data['state']
            cities = state.cities.all()
            if city not in cities:
                raise ValueError('Provided city not in state.')

        if 'city' in validated_data and 'state' not in validated_data:
            city = validated_data['city']
            state = car_advert_instance.state
            if state != city.state:
                raise ValueError('Provided city not in state.')

    def validate_brand_model(self, validated_data, car_advert_instance):
        """This method enforces brand and model foreign key relationship."""
        if 'model' in validated_data and 'brand' in validated_data:
            model = validated_data['model']
            brand = validated_data['brand']
            brand_models = brand.brand_models.all()
            if model not in brand_models:
                raise ValueError('Provided car model not in car brand.')

        # Enforce brand and model relationship in the car_adverts table.
        if 'model' in validated_data and 'brand' not in validated_data:
            model = validated_data['model']
            brand = car_advert_instance.brand
            if brand != model.brand:
                raise ValueError('Provided car model not in car brand.')

    def validate_server_images(self, validated_data, car_advert_instance):
        """This method validates images saved on the server."""
        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.get('uploaded_images')

            uploaded_cloud_images = validated_data.get('uploaded_cloud_images')

            if uploaded_images and uploaded_cloud_images:
                raise ValueError('You can either save images '\
                                'to the cloud or server, but not both.')

            if len(uploaded_images) > 10:
                raise ValueError('Uploaded images cannot be more than 10.')

            images = car_advert_instance.images.all()
            if len(images) + len(uploaded_images) > 10:
                error_message = 'Uploaded images cannot be more than 10, '\
                                'either delete previous uploaded images '\
                                'or reduce the number of new images to be uploaded.'
                raise ValueError(error_message)

            if len(images) + len(uploaded_images) < 5:
                raise ValueError('Uploaded images cannot be less than 5.')

            for image in images:
                if image.cloud_image is not None and image.cloud_image != '':
                    error_message = 'Images were previously '\
                                    'saved on the cloud server, '\
                                    'delete completely to save '\
                                    'on the server for this advert.'
                    raise ValueError(error_message)

            validated_data['is_cloud_server_images'] = False

    def validate_cloud_images(self, validated_data, car_advert_instance):
        """This method validates images saved on the cloud."""
        if 'uploaded_cloud_images' in validated_data:
            uploaded_cloud_images = validated_data.get('uploaded_cloud_images')

            uploaded_images = validated_data.get('uploaded_images')

            if uploaded_cloud_images and uploaded_images:
                raise ValueError('You can either save images '\
                                'to the cloud or server, but not both.')

            if len(uploaded_cloud_images) > 10:
                raise ValueError('Uploaded images cannot be more than 10.')

            images = car_advert_instance.images.all()
            if len(images) + len(uploaded_cloud_images) > 10:
                error_message = 'Uploaded images cannot be more than 10, '\
                                'either delete previous uploaded images '\
                                'or reduce the number of new images to be uploaded.'
                raise ValueError(error_message)

            if len(images) + len(uploaded_cloud_images) < 5:
                raise ValueError('Uploaded images cannot be less than 5.')

            for image in images:
                if image.image is not None and image.image != '':
                    error_message = 'Images were previously '\
                                    'saved on the server, '\
                                    'delete completely to save '\
                                    'on the cloud for this advert.'
                    raise ValueError(error_message)

            validated_data['is_cloud_server_images'] = True

    def validate_server_thumbnail(self, validated_data, car_advert_instance):
        """This method validates image thumbnail saved on the server."""
        if 'thumbnail' in validated_data:
            if car_advert_instance.thumbnail_cloud is not None and \
                car_advert_instance.thumbnail_cloud != '':
                error_message = 'Thumbnail was previously '\
                                'saved on the cloud, '\
                                'delete it to save '\
                                'on the server for this advert.'
                raise ValueError(error_message)

            thumbnail = validated_data.get('thumbnail')
            thumbnail_cloud = validated_data.get('thumbnail_cloud')

            if not thumbnail:
                raise ValueError('Thumbnail cannot be empty.')

            if thumbnail and thumbnail_cloud:
                raise ValueError('You can either save images '\
                                'to the cloud or server, but not both.')

            validate_mimetype(thumbnail)

            validated_data['is_cloud_server_thumbnail'] = False

    def validate_cloud_thumbnail(self, validated_data, car_advert_instance):
        """This method validates image thumbnail saved on the cloud server."""
        if 'thumbnail_cloud' in validated_data:
            if car_advert_instance.thumbnail is not None and \
                car_advert_instance.thumbnail != '':
                error_message = 'Thumbnail was previously '\
                                'saved on the server, '\
                                'delete it to save '\
                                'on the cloud for this advert.'
                raise ValueError(error_message)

            thumbnail_cloud = validated_data.get('thumbnail_cloud')
            thumbnail = validated_data.get('thumbnail')

            if not thumbnail_cloud:
                raise ValueError('Thumbnail cannot be empty.')

            if thumbnail and thumbnail_cloud:
                raise ValueError('You can either save images '\
                                'to the cloud or server, but not both.')

            validated_data['is_cloud_server_thumbnail'] = True

    def generate_tag_values(self, car_advert_instance):
        """
        This method generates values for the tag column of each instance
        in the car_adverts table.
        """
        year = car_advert_instance.year.year
        brand_name = car_advert_instance.brand.name
        model_name = car_advert_instance.model.name
        state_name = car_advert_instance.state.name
        city_name = car_advert_instance.city.name
        user_name = car_advert_instance.user.username
        fuel_type = car_advert_instance.fuel_type

        car_advert_instance.tag = f'{year}, {brand_name}, {model_name}, {fuel_type}, '\
                    f'{state_name}, {city_name}, {user_name}'

    def save_multiple_server_images(self, uploaded_images, image_model, car_advert_instance):
        """
        This method saves multiple images with a foreign key
        relationship to an advert instance to the server and database.
        On error it deletes all saved images and returns a response.
        """
        for image in uploaded_images:
            try:
                validate_mimetype(image)
                image_instances = []
                new_image = image_model(car_advert=car_advert_instance, image=image)
                new_image.save()
                image_instances.append(new_image)
            except Exception as error: # pylint: disable=broad-exception-caught
                for image_instance in image_instances:
                    image_instance.delete()
                return JsonResponse({'error': str(error)}, status=400)

    def save_multiple_cloud_images(self, uploaded_cloud_images, image_model, car_advert_instance):
        """
        This method saves multiple cloud images with a foreign key
        relationship to an advert instance to the database.
        On error it deletes all saved images and returns a response.
        """
        for image in uploaded_cloud_images:
            try:
                image_instances = []
                new_image = image_model(car_advert=car_advert_instance, cloud_image=image)
                new_image.save()
                image_instances.append(new_image)
            except Exception as error: # pylint: disable=broad-exception-caught
                for image_instance in image_instances:
                    image_instance.delete()
                return JsonResponse({'error': str(error)}, status=400)

    def get(self, request, pk):
        """
        This method returns the request.data of one instance of the CarAdvert model if
        the provided id matches any in the database. It also returns a http status
        code of 400 if provided id fails to match any of the ids in the database.
        """
        try:
            advert = CarAdvert.objects.get(id=pk)
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        serializer = CarAdvertSerializer(advert)
        return JsonResponse(serializer.data, status=200)

    def delete(self, request, pk):
        """
        This method deletes an instance of the CarAdvert model if the provided id
        matches any in the database.
        """
        try:
            advert = CarAdvert.objects.get(id=pk)
            user = advert.user
            advert_user_id = advert.user.id
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, _ = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == advert_user_id:
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
                    activity_type = 'Delete',
                    activity_details = f'Deleted advert: {advert.id}',
                )

                message = f'Advert {advert.id} deleted successfully.'
                advert.delete()

                return JsonResponse({'message': message}, status=200)

            if user_id != advert_user_id:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message

    def put(self, request, pk): # pylint: disable=redefined-builtin
        """This method updates all the fields of an instance of the CarAdvert model."""
        self.parser_classes = [JSONParser, MultiPartParser, FormParser]
        try:
            advert = CarAdvert.objects.get(id=pk)
            user = advert.user
            advert_user_id = advert.user.id
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        # decode access token using the decode_token function
        result = decode_token(request)

        if isinstance(result, JsonResponse):
            return result

        user_id, is_superuser, is_manager = result

        manager = user.team_manager if hasattr(user, 'team_manager') else None
        if manager:
            user_manager = True if manager.id == user_id else False
        else:
            user_manager = False

        if user_manager is True or is_superuser is True or user_id == advert_user_id:
            serializer = CarAdvertSerializer(advert, data=request.data, partial=True)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                try:
                    self.validate_brand_model(validated_data, advert)
                    self.validate_state_city(validated_data, advert)
                    self.validate_server_images(validated_data, advert)
                    self.validate_cloud_images(validated_data, advert)
                    self.validate_server_thumbnail(validated_data, advert)
                    self.validate_cloud_thumbnail(validated_data, advert)
                except Exception as error_message: # pylint: disable=broad-exception-caught
                    return JsonResponse({'error': str(error_message)}, status=400)

                # restrict only a marketer from updating the user(owner) of an advert.
                if user_id == advert_user_id and is_superuser is False and is_manager is False:
                    uneditable_fields = ('user',)
                    for field in uneditable_fields:
                        if field in validated_data:
                            error_message = 'You do not have the permission '\
                                            'to perform this action.'
                            return JsonResponse({'error': error_message}, status=403)

                if 'uploaded_images' in validated_data:
                    uploaded_images = validated_data.pop('uploaded_images')

                    if uploaded_images:
                        upload_error = self.save_multiple_server_images(uploaded_images, Image,
                                                                        advert)
                        if upload_error:
                            return upload_error

                if 'uploaded_cloud_images' in validated_data:
                    uploaded_cloud_images = validated_data.pop('uploaded_cloud_images')

                    if uploaded_cloud_images:
                        upload_error = self.save_multiple_cloud_images(uploaded_cloud_images, Image,
                                                                       advert)
                        if upload_error:
                            return upload_error

                for attr, value in validated_data.items():
                    setattr(advert, attr, value)

                self.generate_tag_values(advert)

                advert.save()

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
                    activity_type = 'Update',
                    activity_details = f'Updated advert: {advert.id}',
                )

                serializer = CarAdvertSerializer(advert)
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        if user_id != advert_user_id:
            error_message = 'You do not have the permission to perform this action.'
            return JsonResponse({'error': error_message}, status=403)
