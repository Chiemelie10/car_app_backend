"""This module defines the class MarketerRegisterationView."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from car_app.views.views_helper_functions import password_hasher, decode_token
from car_app.serializers.middleware.validate_user import validate_user
from car_app.models import User
from car_app.serializers.user_serializer import GetUserSerializer
from user_activity.models import UserActivity
from drf_spectacular.utils import extend_schema


class MarketerRegistrationView(APIView):
    """Defines a method for creating a new user(marketer)."""

    permission_classes = [IsAdminUser]
    serializer_class = GetUserSerializer

    @extend_schema(
        request={"application/json": {"example":
                                      {"username": "example_user",
                                       "password": "secret_password",
                                       "email": "example@gmail.com",
                                       "first_name": "user_first_name",
                                       "last_name": "user_last_name",
                                       "phone_number": "07058679688"}}}
    )
    @method_decorator(validate_user)
    def post(self, request, validated_data):
        """
        This method hashes the provided password and saves
        a user to the database.
        """
        # pylint: disable=no-member

        result = decode_token(request)
        if isinstance(result, tuple):
            user_id, _, _ = result

            try:
                staff_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Provided token has no valid user.'},
                                    status=401)

            hashed_password = password_hasher(validated_data)
            validated_data['password'] = hashed_password
            validated_data['is_marketer'] = True

            referral_code = validated_data.get('referral_code')

            if referral_code is None:
                referral_code = staff_user.manager_code
                validated_data['referral_code'] = referral_code

            try:
                team_manager = User.objects.get(manager_code=referral_code)
                validated_data['team_manager'] = team_manager
                user = User(**validated_data)
                user.save()
                serializer = GetUserSerializer(user)

                UserActivity.objects.create(
                    user = staff_user,
                    activity_type = 'Create',
                    activity_details = f'New user: {user.id}',
                )

                return JsonResponse(serializer.data, status=201)
            except User.DoesNotExist:
                error_message = 'Invalid referral code, remove field if not certain.'
                return JsonResponse({'error': error_message}, status=400)
            except IntegrityError as error:
                if 'email' in str(error):
                    return JsonResponse({'error': 'Email not available.'}, status=400)
                if 'username' in str(error):
                    return JsonResponse({'error': 'Username not available.'}, status=400)
            except BaseException as error: # pylint: disable=broad-exception-caught
                return JsonResponse({'error': str(error)}, status=400)

        error_message = result
        return error_message
