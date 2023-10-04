"""This module defines class DeleteImage"""
import os
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.http import JsonResponse
from image.models import Image
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from user_activity.models import UserActivity


class DeleteImage(APIView):
    """This class defines a method to delete an image"""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, image_id):
        """
        This method deletes a an image from the database and location
        it was saved in the server.
        """
        result = decode_token(request)

        if isinstance(request, JsonResponse):
            return request

        user_id, is_superuser, _ = result

        try:
            image_to_delete = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image not found'}, status=404)

        image_owner = image_to_delete.car_advert.user

        manager = image_owner.team_manager if hasattr(image_owner, 'team_manager') else None
        if manager:
            image_owner_manager = True if manager.id == user_id else False
        else:
            image_owner_manager = False

        if image_owner_manager is True or is_superuser is True or user_id == image_owner.id:
            relative_path = image_to_delete.image
            absolute_path = os.path.join(settings.MEDIA_ROOT, f'{relative_path}')

            if is_superuser is True:
                try:
                    action_performing_user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Provided token has no valid user.'}, 401)
            elif image_owner_manager is True:
                action_performing_user = manager
            else:
                action_performing_user = image_owner

            user_activity = UserActivity.objects.create(
                user = action_performing_user,
                activity_type = 'Delete',
                activity_details = f'Deleted image: {image_to_delete.id}',
            )

            if os.path.exists(absolute_path):
                os.remove(path=absolute_path)
                image_to_delete.delete()
            else:
                user_activity.delete()
                return JsonResponse({'error': 'Image found in database but not on server.'},
                                    status=500)

            return JsonResponse({'message': 'Image deleted successfully.'}, status=200)

        if user_id != image_owner.id:
            error_message = 'You do not have the permission to perform this action.'
            return JsonResponse({'error': error_message}, status=403)
