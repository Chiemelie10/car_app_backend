"""This module defines class GetUserAdverts.py"""
from rest_framework.views import APIView
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from car_app.models import User
from car_advert.serializers import CarAdvertSerializer
from car_advert.utils import paginate_queryset


class GetUserAdverts(APIView):
    """This class defines a method to get adverts belonging to a user."""
    # pylint: disable=no-member
    # pylint: disable=unused-argument

    serializer_class = CarAdvertSerializer

    def get(self, request, user_id):
        """This method gets adverts depending on the provided user_id."""
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page size values.'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            adverts = user.adverts.filter(is_active=True).order_by('created_at')
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=400)

        result = paginate_queryset(adverts, page, page_size)

        if isinstance(result, JsonResponse):
            return result

        paginated_data, total_pages = result
        serializer = CarAdvertSerializer(paginated_data, many=True)

        if page == 1 and page == total_pages:
            previous_page = None
            next_page = None
        elif page == 1 and page < total_pages:
            previous_page = None
            next_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse('get-user-adverts', args=[user_id])}"\
                        f"/?page={page + 1}&page-size={page_size}"
        if page > 1 and page < total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-user-adverts', args=[user_id])}"\
                            f"/?page={page - 1}&page-size={page_size}"
            next_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse('get-user-adverts', args=[user_id])}"\
                        f"/?page={page + 1}&page-size={page_size}"
        if page > 1 and page == total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-user-adverts', args=[user_id])}"\
                            f"/?page={page - 1}&page-size={page_size}"
            next_page = None

        data = {
            'total_adverts': len(adverts),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
            'adverts': serializer.data
        }

        return JsonResponse(data, safe=False, status=200)
