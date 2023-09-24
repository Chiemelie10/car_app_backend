"""This module defines the module SearchAdverts."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer


class SearchAdvert(APIView):
    """This class defines a post method that searches for adverts."""
    # pylint: disable=no-member

    def post(self, request):
        """This method searches for adverts by title, description, fuel_type or tag."""
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be application/json.'})

        search_query = request.data.get('search', '')

        results = CarAdvert.objects.filter(is_active=True).raw(
            'SELECT * FROM car_adverts WHERE MATCH (title, description, tag) '\
            'AGAINST (%s)',[search_query]
        )
        serializer = CarAdvertSerializer(results, many=True)

        return JsonResponse(serializer.data, status=200, safe=False)
