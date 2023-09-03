"""This module defines the function password_hasher."""
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


def password_hasher(data):
    """
    This function returns hashed password if successful, otherwise
    it returns an error.
    """
    password = data.get('password')
    try:
        hashed_password = make_password(password)
    except ValueError as error:
        return JsonResponse({'error': str(error)}, status=400)
    except TypeError as error:
        return JsonResponse({'error': str(error)}, status=400)
    except OverflowError as error:
        return JsonResponse({'error': str(error)}, status=500)

    return hashed_password
