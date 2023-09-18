"""This module defines class GetCities."""
from rest_framework.views import APIView
from django.http import JsonResponse
from city.models import City
from city.serializers import CityModelSerializer


class GetCities(APIView):
    """
    This class defines a method that returns all instances
    of City model from the database.
    """
    # pylint: disable=unused-argument

    def get(self, request):
        """
        This method returns all instances of the City model
        from the database.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            cities = City.objects.all()
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = CityModelSerializer(cities, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
