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

    serializer_class = CarAdvertSerializer

    def get(self, request):
        """
        This method returns all instances of the CarAdvert module in the database.
        """
        # pylint: disable=broad-exception-caught
        # pylint: disable=no-member

        page = request.GET.get('page')
        page_size = request.GET.get('page-size')

        if not page_size and not page:
            try:
                adverts = CarAdvert.objects.all().order_by('created_at')
            except Exception as error:
                return JsonResponse({'error': str(error)}, status=500)

            serializer = CarAdvertSerializer(adverts, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)

        if page and not page_size:
            return JsonResponse({'error': 'Page size is needed.'}, status=400)

        if page_size and not page:
            page = 1

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page size values.'}, status=400)

        try:
            adverts = CarAdvert.objects.all().order_by('created_at')
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=500)

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
                        f"{reverse('get-adverts')}/?page={page + 1}&page-size={page_size}"
        if page > 1 and page < total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-adverts')}/?page={page - 1}"\
                            f"&page-size={page_size}"
            next_page = f"https://{get_current_site(request).domain}"\
                        f"{reverse('get-adverts')}/?page={page + 1}&page-size={page_size}"
        if page > 1 and page == total_pages:
            previous_page = f"https://{get_current_site(request).domain}"\
                            f"{reverse('get-adverts')}/?page={page - 1}"\
                            f"&page-size={page_size}"
            next_page = None

        data = {
            'total_adverts': len(adverts),
            'total_pages': total_pages,
            'previous_page': previous_page,
            'next_page': next_page,
            'adverts': serializer.data
        }
        return JsonResponse(data, status=200, safe=False)
