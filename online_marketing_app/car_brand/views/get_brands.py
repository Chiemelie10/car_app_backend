"""This module defines class GetBrands."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_brand.models import CarBrand
from car_brand.serializers import CarBrandSerializer


class GetBrands(APIView):
    """
    This class defines a method that returns all instances
    of CarBrand in the database.
    """
    # pylint: disable=unused-argument
    serializer_class = CarBrandSerializer

    def get(self, request):
        """
        This method returns all instances of the CarBrand model
        in the database.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            brands = CarBrand.objects.all()
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = CarBrandSerializer(brands, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
