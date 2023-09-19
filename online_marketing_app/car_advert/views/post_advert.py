"""This module defines class PostAdvert."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_app.views.views_helper_functions import decode_token
from image.models import Image


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
                    manager = True if manager.id == user_id else False

                if manager is True or is_superuser is True:
                    car_advert = CarAdvert(**validated_data)
                    car_advert.save()

                    for image in uploaded_images:
                        Image.objects.create(car_advert=car_advert, image=image)
                    serializer = CarAdvertSerializer(car_advert)
                    return JsonResponse(serializer.data, status=201)

                if manager is False or manager is None:
                    error_message = 'You do not have the permission to perform this action.'
                    return JsonResponse({'error': error_message}, status=403)
        return JsonResponse(serializer.errors, status=400)
