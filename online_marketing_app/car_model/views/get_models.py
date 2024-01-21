"""This module defines class GetModels."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_model.models import CarModel
from car_model.serializers import CarModelSerializer


class GetModels(APIView):
    """
    This class defines a method that returns all instances
    of CarModel from the database.
    """
    # pylint: disable=unused-argument

    serializer_class = CarModelSerializer

    def get(self, request):
        """
        This method returns all instances of the CarModel model
        from the database.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            models = CarModel.objects.all()
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = CarModelSerializer(models, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
