"""This module defines class GetStates."""
from rest_framework.views import APIView
from django.http import JsonResponse
from state.models import State
from state.serializers import StateModelSerializer


class GetStates(APIView):
    """
    This class defines a method that returns all instances
    of State model from the database.
    """
    # pylint: disable=unused-argument

    def get(self, request):
        """
        This method returns all instances of the State model
        from the database.
        """
        #pylint: disable=broad-exception-caught
        #pylint: disable=no-member

        try:
            states = State.objects.all()
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        serializer = StateModelSerializer(states, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
