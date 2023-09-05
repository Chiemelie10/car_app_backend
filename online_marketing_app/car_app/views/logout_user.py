"""This module defines class UserLogout."""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import JsonResponse


class UserLogout(APIView):
    """
    This class defines a method that logout a user from
    the application.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This method blacklists refresh token when a user logs out."""
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        try:
            refresh = request.data.get('refresh')
            token = RefreshToken(refresh)
            token.blacklist()
            return JsonResponse({'message': 'Logged out successfully.'}, status=200)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'error': str(error)}, status=400)
