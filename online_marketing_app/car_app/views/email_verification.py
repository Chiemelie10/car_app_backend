"""This module defines class VerifyEmail."""
from os import getenv
import jwt
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from dotenv import load_dotenv
from car_app.models import User
from car_app.views.views_helper_functions import decode_token
from car_app.utils import Util
from user_activity.models import UserActivity


load_dotenv()


class VerifyEmail(APIView):
    """This class defines a method confirms email verification."""
    def get(self, request):
        """
        This method sets the is_verified field of the User model to true
        in the database if successful, otherwise it returns a http status
        code of 400 with the corresponding error message.
        """
        # pylint: disable=no-member

        token = request.GET.get('token')
        try:
            secret_key = getenv('PROJECT_SECRET_KEY')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if user.is_verified is False:
                user.is_verified = True
                user.save()

            UserActivity.objects.create(
                user = user,
                activity_type = 'Verification',
            )

            return JsonResponse({'message': 'Email verified successfully.'}, status=200)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'The link has expired.'}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'error': 'The link is invalid'}, status=400)
        except User.DoesNotExist: # pylint: disable=no-member
            return JsonResponse({'error': 'The link is invalid'}, status=400)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'error': str(error)}, status=400)


class SendEmailVerificationLink(APIView):
    """
    This class defines the method that handles sending of email
    verification links.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """This method sends email verification link to a registered user."""
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be json.'})

        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, _, _, = result
        else:
            return result

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist: # pylint: disable=no-member
            error_message = 'The user authenticated with the provided '\
                            'token was not found in the database.'
            return JsonResponse({'error': error_message}, status=400)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        current_site = get_current_site(request).domain
        relative_link = reverse('email_verify')
        abs_url = 'http://' + current_site + relative_link + '?token=' + access
        email_body = 'Hi ' + user.username + ', click on the link below to verify your email.\n' + abs_url

        data = {
            'email_subject': 'Verify your email',
            'email_body': email_body,
            'to_email': user.email
        }

        try:
            Util.send_email(data)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'errot': str(error)}, status=400)

        return JsonResponse({'message': 'The verification link was sent successfully'}, status=200)
