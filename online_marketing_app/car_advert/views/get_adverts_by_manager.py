"""This module defines class GetManagerAdvert."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.serializers import CarAdvertSerializer
from car_advert.models import CarAdvert
from car_app.models import User


class GetManagerAdvert(APIView):
    """
    This class defines methods to get all active car adverts managed by a manager.
    """
    # pylint: disable=unused-argument
    # pylint: disable=no-member

    serializer_class = CarAdvertSerializer

    def get(self, request, manager_id):
        """
        This method returns all adverts managed by a user
        """
        try:
            user = User.objects.get(id=manager_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=400)

        if user.is_manager is False:
            return JsonResponse({'error': 'User must be a found.'}, status=401)

        adverts = CarAdvert.objects.filter(
            user__team_manager=user,
            is_active=True,
        ).order_by('created_at')

        serializer = CarAdvertSerializer(adverts, many=True)
        print(serializer)
        return JsonResponse(serializer.data, status=200, safe=False)
