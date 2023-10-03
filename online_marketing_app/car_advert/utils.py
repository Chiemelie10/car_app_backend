"""This module contains functions utilised in the app"""
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def paginate_queryset(queryset, page, page_size):
    """
    This function defines the number of adverts to be returned
    per page.
    """
    paginator = Paginator(queryset, per_page=page_size, orphans=0)
    try:
        paginated_data = paginator.page(page)
        total_pages = paginator.num_pages
        return paginated_data, total_pages
    except EmptyPage:
        return JsonResponse({'error': 'Page not found.'}, status=404)
    except PageNotAnInteger:
        return JsonResponse({'error': 'Page number must be an integer.'}, status=400)
