"""This module defines class UserLogin."""
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class UserLogin(APIView):
    """This class defines a method for user login"""
    def post(self, request):
        """
        This method returns access and refresh tokens for a user
        if the provided data for login is found in the database.
        It returns a http error code of 400 if the provided data
        for login is not found in the database.
        """
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

        username = request.data.get('username')
        password = request.data.get('password')
        if username is None:
            return JsonResponse({'error': 'Username must be provided.'}, status=400)
        if password is None:
            return JsonResponse({'error': 'Password must be provided.'}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'error': 'User not found.'}, status=400)

        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['is_superuser'] = user.is_superuser
        access = str(refresh.access_token)

        response = JsonResponse({'access': access}, status=200)
        response.set_cookie('refresh', str(refresh), httponly=True)

        user.last_login = timezone.now()
        user.save()

        return response
