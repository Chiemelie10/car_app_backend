"""This module defines the class GetDeleteUpdateUser."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.http import JsonResponse
from car_app.views.views_helper_functions import decode_token, password_hasher
from car_app.models import User
from car_app.utils import generate_ref_code
from car_app.serializers.user_serializer import GetUserSerializer, UserModelSerializer
from user_activity.models import UserActivity


class GetDeleteUpdateUser(APIView):
    """
    This class defines methods to get, delete or update user data
    in the database.
    """
    # pylint: disable=invalid-name
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        This method returns a user's data if the provided id matches any in the
        database. It also returns a status code of 400 if provided id fails to
        match any of the ids in the database.
        """
        try:
            user_queryset = User.objects.get(pk=pk)
            serializer = GetUserSerializer(user_queryset)
            return JsonResponse(serializer.data, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)

    def delete(self, request, pk):
        """
        This method deletes a user's data if the provided id matches any in the database.
        It also returns an error status code of 400 if provided id fails to
        match any of the ids in the database.
        """
        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, _ = result

            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                error_message = 'User not found.'
                return JsonResponse({'error': error_message}, status=400)

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == pk:
                try:
                    outstanding_tokens = OutstandingToken.objects.filter(user=user)
                    for token in outstanding_tokens:
                        BlacklistedToken.objects.create(token=token)
                except BaseException as error: # pylint: disable=broad-exception-caught
                    return JsonResponse({'error': str(error)}, status=500)

                if is_superuser is True:
                    try:
                        action_performing_user = User.objects.get(id=user_id)
                    except User.DoesNotExist:
                        return JsonResponse({'error': 'Provided token has no valid user.'}, 401)
                elif user_manager is True:
                    action_performing_user = manager
                else:
                    action_performing_user = user

                UserActivity.objects.create(
                    user = action_performing_user,
                    activity_type = 'Delete',
                    activity_details = f'Deleted user: {user.id}',
                )

                message = f'Account for {user.username} has been deleted successfully.'
                user.delete()

                return JsonResponse({'message': message}, status=200)

            if user_id != pk:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message

    def put(self, request, pk):
        """
        This method updates the user data if the provided data matches
        any in the database.
        """
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Content-Type must be json.'}, status=415)

        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, is_manager = result

            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found.'}, status=400)

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == pk:
                serializer = UserModelSerializer(user, data=request.data, partial=True)

                if serializer.is_valid():
                    valid_data = serializer.validated_data

                    if user_id == pk and is_superuser is False and is_manager is False:
                        uneditable_fields = ('is_superuser', 'is_manager', 'is_staff',
                                             'is_active', 'is_marketer', 'is_verified',
                                             'referral_code', 'team_manager', 'groups',
                                             'user_permissions')
                        for field in uneditable_fields:
                            if field in valid_data:
                                error_message = 'You do not have the permission '\
                                                'to perform this action.'
                                return JsonResponse({'error': error_message}, status=403)

                    if user_manager is True and is_superuser is False:
                        uneditable_fields = ('is_superuser', 'is_manager', 'is_staff')
                        for field in uneditable_fields:
                            if field in valid_data:
                                error_message = 'You do not have the permission '\
                                                'to perform this action.'
                                return JsonResponse({'error': error_message}, status=403)

                    if user_id == pk and is_manager is True and is_superuser is False:
                        uneditable_fields = ('is_superuser', 'is_manager', 'is_staff')
                        for field in uneditable_fields:
                            if field in valid_data:
                                error_message = 'You do not have the permission '\
                                                'to perform this action.'
                                return JsonResponse({'error': error_message}, status=403)

                    if 'password' in valid_data:
                        hashed_password = password_hasher(valid_data)
                        valid_data['password'] = hashed_password

                    if 'is_manager' in valid_data:
                        value = valid_data['is_manager']
                        if value is True:
                            code = generate_ref_code()
                            setattr(user, 'manager_code', code)
                            setattr(user, 'team_manager', None)
                            setattr(user, 'is_staff', True)
                        else:
                            setattr(user, 'manager_code', None)
                            setattr(user, 'is_staff', False)
                            users = user.managed_users.all()
                            for managed_user in users:
                                setattr(managed_user, 'team_manager', None)
                                setattr(managed_user, 'referral_code', None)
                                managed_user.save()

                    if 'referral_code' in valid_data:
                        referral_code = valid_data['referral_code']
                        try:
                            user_team_manager = User.objects.get(manager_code=referral_code)
                            setattr(user, 'team_manager', user_team_manager)
                        except User.DoesNotExist:
                            return JsonResponse({'error': 'Invalid referral code.'}, status=400)

                    if 'team_manager' in valid_data:
                        team_manager = valid_data['team_manager']
                        referral_code = team_manager.manager_code
                        if not referral_code:
                            return JsonResponse({'error': f'User {team_manager.id} not a manager.'},
                                                status=400)
                        if referral_code:
                            setattr(user, 'referral_code', referral_code)

                    for attr, value in valid_data.items():
                        setattr(user, attr, value)

                    user.save()
                    serializer = GetUserSerializer(user)

                    if is_superuser is True:
                        try:
                            action_performing_user = User.objects.get(id=user_id)
                        except User.DoesNotExist:
                            return JsonResponse({'error': 'Provided token has no valid user.'}, 401)
                    elif user_manager is True:
                        action_performing_user = manager
                    else:
                        action_performing_user = user

                    UserActivity.objects.create(
                        user = action_performing_user,
                        activity_type = 'Update',
                        activity_details = f'Updated account: {user.id}'
                    )

                    return JsonResponse(serializer.data, status=200)

                return JsonResponse(serializer.errors, status=400)

            if user_id != pk:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message
