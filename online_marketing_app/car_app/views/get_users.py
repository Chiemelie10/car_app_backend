"""This module defines class GetUsers."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_app.serializers.user_serializer import GetUserSerializer
from car_app.models import User


class GetUsers(APIView):
    """
    This class defines a method to get all registered
    users of the application.
    """
    # pylint: disable=unused-argument
    serializer_class = GetUserSerializer

    def get(self, request):
        """
        This method returns all registered users. It also returns
        an empty list if no user is found.
        """
        users = User.objects.all().order_by('created_at')

        if users.exists():
            serializer = GetUserSerializer(users, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        return JsonResponse([], status=200, safe=False)
