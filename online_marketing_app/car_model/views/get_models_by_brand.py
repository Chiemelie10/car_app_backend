"""This module defines class ModelsByBrand."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_model.serializers import CarModelSerializer
from car_brand.models import CarBrand


class ModelsByBrand(APIView):
    """This class defines a method to get models depending on brand_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, brand_id):
        """This method returns all models of a particular brand."""
        try:
            brand = CarBrand.objects.get(id=brand_id)
            models = brand.brand_models.all()
            serializer = CarModelSerializer(models, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except CarBrand.DoesNotExist:
            return JsonResponse({'error': 'Car brand not found.'}, status=404)
