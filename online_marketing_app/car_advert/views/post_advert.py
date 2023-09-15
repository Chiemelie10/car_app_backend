"""This module defines class PostAdvert."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
# from django.http import JsonResponse
# from car_advert.models import CarAdvert
# from car_advert.serializers import CarAdvertSerializer


class PostAdvert(APIView):
    """This class creates a new car advert in the database."""

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None): # pylint: disable=redefined-builtin
        """
        This method validates a post request from api/create-advert route
        and saves it to the database if successful.
        """
        # data = request.data
