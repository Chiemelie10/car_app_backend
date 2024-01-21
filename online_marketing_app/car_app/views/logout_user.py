"""This module defines class UserLogout."""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse
from user_activity.models import UserActivity
from car_app.models import User
from car_app.views.views_helper_functions import decode_token, decode_refresh_token
from drf_spectacular.utils import extend_schema


class UserLogout(APIView):
    """
    This class defines a method that logout a user from
    the application.
    """
    #pylint: disable=no-member

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
            request={"application/json": {"example": {"refresh": "refresh_token"}}},
            responses={200: {"example": {"message": "Logged out successfully."}}},
    )

    def post(self, request):
        """This method blacklists refresh token when a user logs out."""
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token is required.'}, status=400)

        result = decode_token(request)
        if isinstance(result, tuple):
            user_id, is_superuser, _ = result

            result = decode_refresh_token(refresh_token)
            if isinstance(result, JsonResponse):
                return result

            refresh_token_user_id = result
            try:
                user_logging_out = User.objects.get(id=refresh_token_user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Provided token has no valid user.'}, status=401)


            manager = user_logging_out.team_manager if hasattr(
                user_logging_out, 'team_manager') else None

            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if refresh_token_user_id != user_id and is_superuser is False and user_manager is False:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                UserActivity.objects.create(
                    user = user_logging_out,
                    activity_type = 'Logout',
                )

                return JsonResponse({'message': 'Logged out successfully.'}, status=200)
            except BaseException as error: # pylint: disable=broad-exception-caught
                return JsonResponse({'error': str(error)}, status=400)

        error_message = result
        return error_message
