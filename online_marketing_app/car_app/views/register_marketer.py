"""This module defines the class MarketerRegisterationView."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from car_app.views.views_helper_functions import password_hasher
from car_app.serializers.middleware.validate_user import validate_user
from car_app.models import User


class MarketerRegistrationView(APIView):
    """Defines a method for creating a new user(marketer)."""

    permission_classes = [IsAdminUser]

    @method_decorator(validate_user)
    def post(self, validated_data):
        """
        This method hashes the provided password and saves
        a user to the database.
        """
        hashed_password = password_hasher(validated_data)
        validated_data['password'] = hashed_password
        validated_data['is_marketer'] = True

        referral_code = validated_data.get('referral_code')

        try:
            if referral_code is not None:
                team_manager = User.objects.get(manager_code=referral_code)
                validated_data['team_manager'] = team_manager
            user = User(**validated_data)
            user.save()
            return JsonResponse({'message': 'Account created successfully.'}, status=201)
        except User.DoesNotExist: #pylint: disable=no-member
            error_message = 'Invalid referral code, remove field if not certain.'
            return JsonResponse({'error': error_message}, status=400)
        except IntegrityError as error:
            if 'email' in str(error):
                return JsonResponse({'error': 'Email not available.'}, status=400)
            if 'username' in str(error):
                return JsonResponse({'error': 'Username not available.'}, status=400)
        except BaseException as error: # pylint: disable=broad-exception-caught
            return JsonResponse({'error': str(error)}, status=400)
