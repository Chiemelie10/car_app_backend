"""This module defines class GetDeleteUpdateAdvert."""
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_app.views.views_helper_functions import decode_token


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
                manager = True if manager.id == user_id else False

            if manager is True or is_superuser is True or user_id == advert_user_id:
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
        self.parser_classes = [MultiPartParser, FormParser]
        try:
            advert = CarAdvert.objects.get(id=pk)
            user = advert.user
            advert_user_id = advert.user.id
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, is_manager = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                manager = True if manager.id == user_id else False

            if manager is True or is_superuser is True or user_id == advert_user_id:
                serializer = CarAdvertSerializer(advert, data=request.data, partial=True)

                if serializer.is_valid():
                    valid_data = serializer.validated_data

                    if user_id == advert_user_id and is_superuser is False and is_manager is False:
                        uneditable_fields = ('user',)
                        for field in uneditable_fields:
                            if field in valid_data:
                                error_message = 'You do not have the permission '\
                                                'to perform this action.'
                                return JsonResponse({'error': error_message}, status=403)

                    if 'city' in valid_data and 'state' in valid_data:
                        city = valid_data['city']
                        state = valid_data['state']
                        cities = state.cities.all()
                        if city not in cities:
                            return JsonResponse({'error': 'Provided city not in state.'},
                                                status=400)

                    if 'city' in valid_data and 'state' not in valid_data:
                        city = valid_data['city']
                        state = advert.state
                        if state != city.state:
                            return JsonResponse({'error': 'Provided city not in state.'},
                                                status=400)

                    if 'model' in valid_data and 'brand' in valid_data:
                        model = valid_data['model']
                        brand = valid_data['brand']
                        brand_models = brand.brand_models.all()
                        if model not in brand_models:
                            return JsonResponse({'error': 'Provided car model not in car brand.'},
                                                status=400)

                    if 'model' in valid_data and 'brand' not in valid_data:
                        model = valid_data['model']
                        brand = advert.brand
                        if brand != model.brand:
                            return JsonResponse({'error': 'Provided car model not in car brand.'},
                                                status=400)

                    for attr, value in valid_data.items():
                        setattr(advert, attr, value)
                    advert.save()
                    serializer = CarAdvertSerializer(advert)
                    return JsonResponse(serializer.data, status=200)
                return JsonResponse(serializer.errors, status=400)
            if user_id != advert_user_id:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message