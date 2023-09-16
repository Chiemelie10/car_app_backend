"""This module defines the class GetDeleteUpdateUser."""
#from os import getenv
#import jwt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.http import JsonResponse
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from car_app.serializers.user_serializer import GetUserSerializer
#from dotenv import load_dotenv


class GetDeleteUpdateUser(APIView):
    """
    This class defines methods to get, delete or update user data
    in the database.
    """
    # pylint: disable=invalid-name
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        This method returns a user's data if the provided id matches any in the
        database. It also returns a status code of 400 if provided id fails to
        match any of the ids in the database.
        """
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
        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser = result

            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                error_message = 'User not found.'
                return JsonResponse({'error': error_message}, status=400)

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            manager = True if manager.id == user_id else False

            if manager is True or is_superuser is True or user_id == pk:
                try:
                    outstanding_tokens = OutstandingToken.objects.filter(user=user)
                    for token in outstanding_tokens:
                        BlacklistedToken.objects.create(token=token)
                except BaseException as error: # pylint: disable=broad-exception-caught
                    return JsonResponse({'error': str(error)}, status=500)

                message = f'Account for {user.username} has been deleted successfully.'
                user.delete()
                return JsonResponse({'message': message}, status=200)

            if user_id != pk:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message
