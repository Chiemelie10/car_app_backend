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
            'SELECT * FROM car_adverts WHERE MATCH (title, description, tag, fuel_type) '\
            'AGAINST (%s)',[search_query]
        )

        search_terms = search_query.split()

        for result in results:
            result.relevance_score = sum(
                1 for term in search_terms if term in result.title or term in result.description \
                or term in result.tag
            )

        sorted_results = sorted(results, key=lambda x: x.relevance_score, reverse=True)

        serializer = CarAdvertSerializer(sorted_results, many=True)

        return JsonResponse(serializer.data, status=200, safe=False)
