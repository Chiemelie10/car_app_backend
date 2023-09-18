"""This module defines class AdvertsByState."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.serializers import CarAdvertSerializer
from state.models import State


class AdvertsByState(APIView):
    """This class defines a method to get adverts depending on state_id"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, state_id):
        """
        This method returns all adverts in a particular state that have
        is_active set true.
        """
        try:
            state = State.objects.get(id=state_id)
            adverts = state.adverts.filter(is_active=True)
            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except State.DoesNotExist:
            return JsonResponse({'error': 'State not found.'}, status=400)
