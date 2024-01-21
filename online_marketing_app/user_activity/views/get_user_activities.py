"""This module defines class GetUserActivity."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from user_activity.models import UserActivity
from user_activity.serializers import UserActivitySerializer
from car_app.models import User
from car_app.views.views_helper_functions import decode_token


class GetUserActivity(APIView):
    """This class defines a method to get all user activities."""

    permission_classes = [IsAdminUser]
    serializer_class = UserActivitySerializer

    def get(self, request):
        """This method returns all user activities."""
        # pylint: disable=no-member

        result = decode_token(request)
        if isinstance(result, tuple):
            user_id, is_superuser, is_manager = result

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Provided token has no valid user.'}, status=401)

            if is_superuser:
                activities = UserActivity.objects.all()
            elif is_manager:
                activities = UserActivity.objects.filter(
                    user__in=[user] + list(user.managed_users.all())).order_by('-timestamp')
            elif user.is_staff and not is_manager:
                activities = UserActivity.objects.filter(user=user)

            serializer = UserActivitySerializer(activities, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        error_message = result
        return error_message
