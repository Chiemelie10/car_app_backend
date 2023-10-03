"""This module defines the function password_hasher."""
from os import getenv
import jwt
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from dotenv import load_dotenv


load_dotenv()


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

def decode_token(request):
    """
    This decodes a jwt token from the Authorization header of a request and
    returns the values of user_id, is_superuser and is_manager.
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION')

    if auth_header:
        token = auth_header.split(' ')[1]
        secret_key = getenv('PROJECT_SECRET_KEY')
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            is_superuser = decoded_token.get('is_superuser')
            is_manager = decoded_token.get('is_manager')
            return user_id, is_superuser, is_manager
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'The token has expired.'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'The token is invalid.'}, status=401)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'error': str(error)}, status=401)
    else:
        return JsonResponse({'error': 'Authorization header is required.'}, status=401)


def decode_refresh_token(request):
    """
    This decodes a jwt refresh token from the cookie in header of a request and
    returns the values of user_id, is_superuser and is_manager.
    """
    refresh_token = request.COOKIES.get('refresh')

    if refresh_token:
        secret_key = getenv('PROJECT_SECRET_KEY')
        try:
            decoded_token = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            return user_id, refresh_token
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'The token has expired.'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'The token is invalid.'}, status=401)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'error': str(error)}, status=401)
    else:
        return JsonResponse({'error': 'Refresh token not found in the cookie.'}, status=401)
