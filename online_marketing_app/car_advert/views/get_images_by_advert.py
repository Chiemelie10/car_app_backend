"""This module defines class ImagesByAdvert."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.models import CarAdvert
from image.serializers import ImageModelSerializer


class ImagesByAdvert(APIView):
    """This class defines a method to get images depending on advert_id."""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    def get(self, request, advert_id):
        """This method returns all images of a particlar advert."""
        try:
            advert = CarAdvert.objects.get(id=advert_id)
            images = advert.images.all()
            serializer = ImageModelSerializer(images, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        except CarAdvert.DoesNotExist:
            return JsonResponse({'error': 'Car advert not found.'}, status=400)
