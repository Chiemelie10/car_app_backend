"""This module defines class AdvertsByModel."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.serializers import CarAdvertSerializer
from car_model.models import CarModel


class AdvertsByModel(APIView):
    """This class defines a method to get adverts depending on model_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, model_id):
        """
        This method returns all adverts of a particular model that have
        is_active set true.
        """
        try:
            model = CarModel.objects.get(id=model_id)
            adverts = model.adverts.filter(is_active=True)
            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except CarModel.DoesNotExist:
            return JsonResponse({'error': 'Car model not found.'}, status=404)
