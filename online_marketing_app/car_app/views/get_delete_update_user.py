"""This module defines the class GetDeleteUpdateUser and AllUsersOperations."""
#from os import getenv
#import jwt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from car_app.serializers.user_serializer import GetUserSerializer
#from dotenv import load_dotenv


#load_dotenv()


class GetDeleteUpdateUser(APIView):
    """
    This class defines methods to get, delete or update user data
    in the database.
    """
    # pylint: disable=invalid-name
    # pylint: disable=no-member

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        This method returns a user's data if the provided id matches any in the database.
        It also returns an error status code of 400 if provided id fails to
        match any of the ids in the database.
        """
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        try:
            user_queryset = User.objects.get(pk=pk)
            serializer = GetUserSerializer(user_queryset)
            return JsonResponse(serializer.data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

    def delete(self, request, pk):
        """
        This method deletes a user's data if the provided id matches any in the database.
        It also returns an error status code of 400 if provided id fails to
        match any of the ids in the database.
        """
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        #auth_header = request.META.get('HTTP_AUTHORIZATION')
        result = decode_token(request)
        refresh = request.data.get('refresh')

        if refresh is None:
            return JsonResponse({'error': 'Refresh token is required.'})

        if isinstance(result, tuple):
            user_id, is_superuser = result
        else:
            error_message = result
            return error_message

        if is_superuser is True or user_id == pk:
            try:
                token = RefreshToken(refresh)
                token.blacklist()
            except BaseException as error: # pylint: disable=broad-exception-caught
                return JsonResponse({'error': str(error)}, status=400)
            user_queryset = User.objects.get(pk=pk)
            user_queryset.delete()
            message = f'Account for {user_queryset.username} has been deleted successfully.'
            return JsonResponse({'message': message}, status=200)
        if user_id != pk:
            return JsonResponse({'error': 'Unauthorized.'}, status=401)
