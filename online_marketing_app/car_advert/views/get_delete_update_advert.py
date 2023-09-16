"""This module defines class GetDeleteUpdateAdvert."""
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_brand.models import CarBrand
from car_model.models import CarModel
from car_manufacture_year.models import ManufactureYear
from car_app.models import User
from car_app.views.views_helper_functions import decode_token
from state.models import State
from city.models import City


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
            user_id, is_superuser = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
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
            user_id, is_superuser = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            manager = True if manager.id == user_id else False

            if manager is True or is_superuser is True or user_id == advert_user_id:
                serializer = CarAdvertSerializer(advert, data=request.data, partial=True)

                if serializer.is_valid():
                    valid_data = serializer.validated_data
                    if 'brand' in valid_data:
                        try:
                            brand = CarBrand.objects.get(id=valid_data['brand'])
                            valid_data['brand'] = brand
                        except CarBrand.DoesNotExist:
                            return JsonResponse({'error': 'Brand not found.'}, status=400)

                    if 'model' in valid_data:
                        try:
                            model = CarModel.objects.get(id=valid_data['model'])
                            valid_data['model'] = model
                        except CarModel.DoesNotExist:
                            return JsonResponse({'error': 'Model not found.'}, status=400)

                    if 'year' in valid_data:
                        try:
                            year = ManufactureYear.objects.get(id=valid_data['year'])
                            valid_data['year'] = year
                        except CarModel.DoesNotExist:
                            return JsonResponse({'error': 'Year not found.'}, status=400)

                    if 'state' in valid_data:
                        try:
                            state = State.objects.get(id=valid_data['state'])
                            valid_data['state'] = state
                        except CarModel.DoesNotExist:
                            return JsonResponse({'error': 'State not found.'}, status=400)

                    if 'city' in valid_data:
                        try:
                            city = City.objects.get(id=valid_data['city'])
                            valid_data['city'] = city
                        except City.DoesNotExist:
                            return JsonResponse({'error': 'City not found.'}, status=400)

                    if 'user' in valid_data:
                        try:
                            user = User.objects.get(id=valid_data['user'])
                            valid_data['user'] = user
                        except User.DoesNotExist:
                            return JsonResponse({'error': 'User not found.'})

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
