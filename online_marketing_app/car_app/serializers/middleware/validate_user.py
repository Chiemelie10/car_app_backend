"""This module defines the function validate_user."""
from functools import wraps
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from car_app.serializers.user_serializer import UserModelSerializer


def validate_user(func):
    """
    This function validates registration data and handles
    the error returned by the UserModelSerializer.
    """
    @wraps(func)
    def wrapper_function(request, *args, **kwargs):
        """
        Returns the validated data to the view function if successful,
        otherwise it handles the error returned by the UserModelSerializer
        before it gets the view function.
        """
        if request.method == 'POST':
            if request.content_type != 'application/json':
                return JsonResponse({'error': 'The Content-Type must be json.'}, status=415)

            data = JSONParser().parse(request)
            serializer = UserModelSerializer(data=data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                return func(request, validated_data, *args, **kwargs)

            return JsonResponse(serializer.errors, status=400)
        return JsonResponse({'error': 'Method for the request must be POST.'})
    return wrapper_function
