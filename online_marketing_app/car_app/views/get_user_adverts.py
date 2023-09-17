"""This module defines class GetUserAdverts.py"""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_app.models import User
from car_advert.serializers import CarAdvertSerializer


class GetUserAdverts(APIView):
    """This class defines a method to get adverts belonging to a user."""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, user_id):
        """This method gets adverts depending on the provided user_id."""
        try:
            user = User.objects.get(id=user_id)
            adverts = user.adverts.all()
            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=400)
