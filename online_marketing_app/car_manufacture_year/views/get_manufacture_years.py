"""This module defines class GetManufactureYears."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_manufacture_year.models import ManufactureYear
from car_manufacture_year.serializer import ManufactureYearSerializer


class GetManufactureYears(APIView):
    """
    This class defines a method that returns all instances
    of ManufactureYear model from the database.
    """
    # pylint: disable=unused-argument

    serializer_class = ManufactureYearSerializer

    def get(self, request):
        """
        This method returns all instances of the ManufactureYear model
        from the database.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            years = ManufactureYear.objects.all()
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = ManufactureYearSerializer(years, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
