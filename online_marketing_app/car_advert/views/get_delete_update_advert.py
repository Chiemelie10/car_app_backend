"""This module defines class GetDeleteUpdateAdvert."""
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_app.views.views_helper_functions import decode_token
from car_app.models import User
from image.models import Image
from user_activity.models import UserActivity


class GetDeleteUpdateAdvert(APIView):
    """
    This class defines methods to get, delete or update single
    car advert request.data in the database.
    """
    # pylint: disable=unused-argument
    # pylint: disable=no-member
    # pylint: disable=invalid-name

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """
        This method returns the request.data of one instance of the CarAdvert model if
        the provided id matches any in the database. It also returns a http status
        code of 400 if provided id fails to match any of the ids in the database.
        """
        try:
            advert = CarAdvert.objects.get(id=pk)
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        serializer = CarAdvertSerializer(advert)
        return JsonResponse(serializer.data, status=200)

    def delete(self, request, pk):
        """
        This method deletes an instance of the CarAdvert model if the provided id
        matches any in the database.
        """
        try:
            advert = CarAdvert.objects.get(id=pk)
            user = advert.user
            advert_user_id = advert.user.id
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, _ = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == advert_user_id:
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
                    activity_details = f'Deleted advert: {advert.id}',
                )

                message = f'Advert {advert.id} deleted successfully.'
                advert.delete()

                return JsonResponse({'message': message}, status=200)

            if user_id != advert_user_id:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message

    def put(self, request, pk): # pylint: disable=redefined-builtin
        """This method updates all the fields of an instance of the CarAdvert model."""
        self.parser_classes = [JSONParser, MultiPartParser, FormParser]
        try:
            advert = CarAdvert.objects.get(id=pk)
            user = advert.user
            advert_user_id = advert.user.id
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Advert not found.'}, status=400)

        # decode access token using the decode_token function
        result = decode_token(request)

        if isinstance(result, tuple):
            user_id, is_superuser, is_manager = result

            manager = user.team_manager if hasattr(user, 'team_manager') else None
            if manager:
                user_manager = True if manager.id == user_id else False
            else:
                user_manager = False

            if user_manager is True or is_superuser is True or user_id == advert_user_id:
                serializer = CarAdvertSerializer(advert, data=request.data, partial=True)

                if serializer.is_valid():
                    valid_data = serializer.validated_data

                    # restrict only a marketer from updating the user(owner) of an advert.
                    if user_id == advert_user_id and is_superuser is False and is_manager is False:
                        uneditable_fields = ('user',)
                        for field in uneditable_fields:
                            if field in valid_data:
                                error_message = 'You do not have the permission '\
                                                'to perform this action.'
                                return JsonResponse({'error': error_message}, status=403)

                    # Enforce state and city relationship in the car_adverts table.
                    if 'city' in valid_data and 'state' in valid_data:
                        city = valid_data['city']
                        state = valid_data['state']
                        cities = state.cities.all()
                        if city not in cities:
                            return JsonResponse({'error': 'Provided city not in state.'},
                                                status=400)

                    # Enforce state and city relationship in the car_adverts table.
                    if 'city' in valid_data and 'state' not in valid_data:
                        city = valid_data['city']
                        state = advert.state
                        if state != city.state:
                            return JsonResponse({'error': 'Provided city not in state.'},
                                                status=400)

                    # Enforce brand and model relationship in the car_adverts table.
                    if 'model' in valid_data and 'brand' in valid_data:
                        model = valid_data['model']
                        brand = valid_data['brand']
                        brand_models = brand.brand_models.all()
                        if model not in brand_models:
                            return JsonResponse({'error': 'Provided car model not in car brand.'},
                                                status=400)

                    # Enforce brand and model relationship in the car_adverts table.
                    if 'model' in valid_data and 'brand' not in valid_data:
                        model = valid_data['model']
                        brand = advert.brand
                        if brand != model.brand:
                            return JsonResponse({'error': 'Provided car model not in car brand.'},
                                                status=400)

                    if 'uploaded_images' in valid_data:
                        uploaded_images = valid_data.pop('uploaded_images')

                        if len(uploaded_images) > 10:
                            error_message = 'Uploaded images cannot be more than 10.'
                            return JsonResponse({'error': error_message}, status=400)

                        images = advert.images.all()
                        if len(images) + len(uploaded_images) > 10:
                            error_message = 'Uploaded images cannot be more than 10, '\
                                            'either delete previous uploaded images '\
                                            'or reduce the number of new images to be uploaded.'
                            return JsonResponse({'error': error_message}, status=400)

                        if len(images) + len(uploaded_images) < 5:
                            error_message = 'Uploaded images cannot be less than 5.'
                            return JsonResponse({'error': error_message}, status=400)

                        for image in images:
                            if image.cloud_image is not None:
                                if image.cloud_image != '':
                                    return JsonResponse({'error': 'Images were previously '\
                                                            'saved on the server, '\
                                                            'delete completely to save '\
                                                            'on the cloud for this advert.'},
                                                            status=400)

                        valid_data['is_cloud_server_images'] = False


                        for image in uploaded_images:
                            try:
                                image_instances = []
                                new_image = Image(car_advert=advert, image=image)
                                new_image.save()
                                image_instances.append(new_image)
                            except Exception as error: # pylint: disable=broad-exception-caught
                                for image_instance in image_instances:
                                    image_instance.delete()
                                return JsonResponse({'error': str(error)}, status=400)

                    if 'uploaded_cloud_images' in valid_data:
                        uploaded_cloud_images = valid_data.pop('uploaded_cloud_images')

                        if len(uploaded_cloud_images) > 10:
                            error_message = 'Uploaded images cannot be more than 10.'
                            return JsonResponse({'error': error_message}, status=400)

                        images = advert.images.all()
                        if len(images) + len(uploaded_cloud_images) > 10:
                            error_message = 'Uploaded images cannot be more than 10, '\
                                            'either delete previous uploaded images '\
                                            'or reduce the number of new images to be uploaded.'
                            return JsonResponse({'error': error_message}, status=400)

                        if len(images) + len(uploaded_cloud_images) < 5:
                            error_message = 'Uploaded images cannot be less than 5.'
                            return JsonResponse({'error': error_message}, status=400)

                        for image in images:
                            if image.image is not None:
                                if image.image != '':
                                    return JsonResponse({'error': 'Images were previously '\
                                                            'saved on the server, '\
                                                            'delete completely to save '\
                                                            'on the cloud for this advert.'},
                                                            status=400)

                        valid_data['is_cloud_server_images'] = True

                        for image in uploaded_cloud_images:
                            try:
                                image_instances = []
                                new_image = Image(car_advert=advert, cloud_image=image)
                                new_image.save()
                                image_instances.append(new_image)
                            except Exception as error: # pylint: disable=broad-exception-caught
                                for image_instance in image_instances:
                                    image_instance.delete()
                                return JsonResponse({'error': str(error)}, status=400)


                    if 'thumbnail' in valid_data:
                        if advert.thumbnail_cloud is not None:
                            if advert.thumbnail_cloud != '':
                                return JsonResponse({'error': 'Thumbnail was previously '\
                                                             'saved on the server, '\
                                                             'delete it to save '\
                                                             'on the cloud for this advert.'},
                                                             status=400)
                        thumbnail = valid_data.get('thumbnail')
                        if not thumbnail:
                            return JsonResponse({'error': 'Thumbnail cannot be empty.'},
                                                status=400)
                        valid_data['is_cloud_server_thumbnail'] = False

                    if 'thumbnail_cloud' in valid_data:
                        if advert.thumbnail is not None:
                            if advert.thumbnail != '':
                                return JsonResponse({'error': 'Thumbnail was previously '\
                                                             'saved on the server, '\
                                                             'delete it to save '\
                                                             'on the cloud for this advert.'},
                                                             status=400)
                        thumbnail_cloud = valid_data.get('thumbnail_cloud')
                        if not thumbnail_cloud:
                            return JsonResponse({'error': 'Thumbnail cannot be empty.'},
                                                status=400)
                        valid_data['is_cloud_server_thumbnail'] = True

                    for attr, value in valid_data.items():
                        setattr(advert, attr, value)

                    # update tag
                    year = advert.year.year
                    brand_name = advert.brand.name
                    model_name = advert.model.name
                    state_name = advert.state.name
                    city_name = advert.city.name
                    user_name = advert.user.username
                    fuel_type = advert.fuel_type

                    advert.tag = f'{year}, {brand_name}, {model_name}, {fuel_type}, '\
                                f'{state_name}, {city_name}, {user_name}'

                    advert.save()

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
                        activity_details = f'Updated advert: {advert.id}',
                    )

                    serializer = CarAdvertSerializer(advert)
                    return JsonResponse(serializer.data, status=200)
                return JsonResponse(serializer.errors, status=400)
            if user_id != advert_user_id:
                error_message = 'You do not have the permission to perform this action.'
                return JsonResponse({'error': error_message}, status=403)
        else:
            error_message = result
            return error_message
