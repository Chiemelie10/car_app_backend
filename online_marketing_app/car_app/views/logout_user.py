"""This module defines class UserLogout."""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from user_activity.models import UserActivity
from car_app.models import User
from car_app.views.views_helper_functions import decode_refresh_token


class UserLogout(APIView):
    """
    This class defines a method that logout a user from
    the application.
    """
    #pylint: disable=no-member

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This method blacklists refresh token when a user logs out."""
        # if request.content_type != 'application/json':
        #     return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        result = decode_refresh_token(request)
        if isinstance(result, tuple):
            user_id, refresh_token = result

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Provided token has no valid user.'}, status=401)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                UserActivity.objects.create(
                    user = user,
                    activity_type = 'Logout',
                )

                return JsonResponse({'message': 'Logged out successfully.'}, status=200)
            except BaseException as error: # pylint: disable=broad-exception-caught
                return JsonResponse({'error': str(error)}, status=400)

        error_message = result
        return error_message
