"""This module defines class AdvertsByManufactureYear."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.serializers import CarAdvertSerializer
from car_manufacture_year.models import ManufactureYear


class AdvertsByManufactureYear(APIView):
    """This class defines a method to get adverts depending on year_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, year_id):
        """
        This method returns all adverts of a particular manufacture year
        that have is_active set true.
        """
        try:
            year = ManufactureYear.objects.get(id=year_id)
            adverts = year.adverts.filter(is_active=True)
            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except ManufactureYear.DoesNotExist:
            return JsonResponse({'error': 'Car manufacture year not found.'}, status=400)
