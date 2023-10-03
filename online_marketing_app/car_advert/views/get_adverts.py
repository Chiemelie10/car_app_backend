"""This module defines class GetAdverts."""
from rest_framework.views import APIView
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_advert.utils import paginate_queryset


class GetAdverts(APIView):
    """
    This class defines a method that returns all instances
    of CarAdvert in the database.
    """
    # pylint: disable=unused-argument

    def get(self, request):
        """
        This method returns all instances of the CarAdvert module that
        have 'is_active' field set to true.
        """
        # pylint: disable=broad-exception-caught
        # pylint: disable=no-member

        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', 10)

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page size values.'}, status=400)

        try:
            all_active_adverts = CarAdvert.objects.filter(is_active=True).order_by('created_at')
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

        result = paginate_queryset(all_active_adverts, page, page_size)

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
                        f"{reverse('get-adverts')}/?page={page + 1}&page-size={page_size}"
        if page > 1 and page < total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-adverts')}/?page={page - 1}&page-size={page_size}"
            next_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse('get-adverts')}/?page={page + 1}&page-size={page_size}"
        if page > 1 and page == total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-adverts')}/?page={page - 1}&page-size={page_size}"
            next_page = None

        data = {
            'total_adverts': len(all_active_adverts),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
            'adverts': serializer.data
        }
        return JsonResponse(data, status=200, safe=False)
