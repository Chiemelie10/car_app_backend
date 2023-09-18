"""This module defines class GetAdverts."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer


class GetAdverts(APIView):
    """
    This class defines a method that returns all instances
    of CarAdvert in the database.
    """
    # pylint: disable=unused-argument

    def get(self, request):
        """
        This method returns all instances of the CarAdvert module that
        have 'is_active' field set to true.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            all_active_adverts = CarAdvert.objects.filter(is_active=True)
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = CarAdvertSerializer(all_active_adverts, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
