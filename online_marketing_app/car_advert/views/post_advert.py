"""This module defines class PostAdvert."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from image.models import Image
from user_activity.models import UserActivity


class PostAdvert(APIView):
    """This class creates a new car advert in the database."""
    # pylint: disable=no-member

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """
        This method validates a post request from api/create-advert route
        and saves it to the database if successful.
        """
        serializer = CarAdvertSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            uploaded_images = validated_data.pop('uploaded_images')

            if not uploaded_images or len(uploaded_images) < 5:
                return JsonResponse({'error': 'Uploaded images cannot be less than 5.'},
                                    status=400)
            if len(uploaded_images) > 10:
                return JsonResponse({'error': 'Uploaded images cannot be more than 10.'},
                                    status=400)

            city = validated_data.get('city')
            state = validated_data.get('state')
            cities = state.cities.all()
            if city not in cities:
                return JsonResponse({'error': 'Provided city must have a matching state.'},
                                    status=400)

            model = validated_data.get('model')
            brand = validated_data.get('brand')
            brand_models = brand.brand_models.all()
            if model not in brand_models:
                return JsonResponse({'error': 'Provided car model must have a matching car brand.'},
                                    status=400)

            user = validated_data.get('user')
            if not user:
                return JsonResponse({'error': 'User is required.'}, status=400)

            result = decode_token(request)

            if isinstance(result, tuple):
                user_id, is_superuser, _ = result

                manager = user.team_manager if hasattr(user, 'team_manager') else None
                if manager:
                    user_manager = True if manager.id == user_id else False
                else:
                    user_manager = False

                if user_manager is True or is_superuser is True or user_id == user.id:
                    year = validated_data.get('year').year
                    fuel_type = validated_data.get('fuel_type')
                    brand_name = city.name
                    model_name = model.name
                    state_name = state.name
                    city_name = city.name
                    user_name = user.username

                    validated_data['tag'] = f'{year}, {brand_name}, {model_name}, {fuel_type}, '\
                                            f'{state_name}, {city_name}, {user_name}'

                    car_advert = CarAdvert(**validated_data)
                    car_advert.save()

                    for image in uploaded_images:
                        try:
                            Image.objects.create(car_advert=car_advert, image=image)
                        except Exception as error: # pylint: disable=broad-exception-caught
                            car_advert.delete()
                            return JsonResponse({'error': str(error)}, status=400)

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
