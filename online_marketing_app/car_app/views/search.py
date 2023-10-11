"""This module defines the module SearchUsers."""
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from car_app.models import User
from car_app.serializers.user_serializer import GetUserSerializer
from car_advert.utils import paginate_queryset


class SearchUsers(APIView):
    """This class defines a post method that searches for users."""
    # pylint: disable=no-member

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        This method searches for users by username, first_name, last_name,
        phone_number, email and manager_code.
        """
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'The Content-Type must be application/json.'})

        search_query = request.data.get('search', '')
        page = request.data.get('page', 1)
        page_size = request.data.get('page_size', 10)

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page size values.'}, status=400)

        results = User.objects.all().raw(
            'SELECT * FROM users WHERE MATCH (id, username, first_name, last_name, phone_number, manager_code) '\
            'AGAINST (%s)',[search_query]
        )

        result = paginate_queryset(results, page, page_size)

        if isinstance(result, JsonResponse):
            return result

        paginated_data, total_pages = result
        serializer = GetUserSerializer(paginated_data, many=True)

        if page == 1 and page == total_pages:
            previous_page = None
            next_page = None
        elif page == 1 and page < total_pages:
            previous_page = None
            next_page = page + 1
        if page > 1 and page < total_pages:
            previous_page = page - 1
            next_page = page + 1
        if page > 1 and page == total_pages:
            previous_page = page - 1
            next_page = None

        data = {
            'total_adverts': len(results),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
            'adverts': serializer.data
        }

        return JsonResponse(data, status=200, safe=False)
