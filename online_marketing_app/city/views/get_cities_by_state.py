"""This module defines class CitiesByState."""
from rest_framework.views import APIView
from django.http import JsonResponse
from city.serializers import CityModelSerializer
from state.models import State


class CitiesByState(APIView):
    """This class defines a method to get cities depending on state_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, state_id):
        """This method returns all cities of a particular state."""
        try:
            state = State.objects.get(id=state_id)
            cities = state.cities.all()
            serializer = CityModelSerializer(cities, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except State.DoesNotExist:
            return JsonResponse({'error': 'State not found.'}, status=404)
