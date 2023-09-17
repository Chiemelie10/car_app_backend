"""This module defines class GetUserAdvert.py"""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer


class GetUserAdvert(APIView):
    """This class defines a method to get an advert belonging to a user."""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, user_id, advert_id):
        """This method gets an advert depending on the provided user_id and advert_id."""
        try:
            advert = CarAdvert.objects.get(user_id=user_id, id=advert_id)
            serializer = CarAdvertSerializer(advert)
            return JsonResponse(serializer.data, status=200)
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found'}, status=400)
