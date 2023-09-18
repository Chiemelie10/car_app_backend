"""This module defines class AdvertsByBrand."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.serializers import CarAdvertSerializer
from car_brand.models import CarBrand


class AdvertsByBrand(APIView):
    """This class defines a method to get adverts depending on brand_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, brand_id):
        """
        This method returns all adverts of a particular brand that have
        is_active set true.
        """
        try:
            brand = CarBrand.objects.get(id=brand_id)
            adverts = brand.adverts.filter(is_active=True)
            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except CarBrand.DoesNotExist:
            return JsonResponse({'error': 'Car brand not found.'}, status=400)
