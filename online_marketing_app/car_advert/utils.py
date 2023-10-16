"""This module contains functions utilised in the app"""
import magic
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

def validate_mimetype(image):
    """
    This function raises ValueError if the file mimetype is not one of the ones
    allowed by the appliaction. 
    """
    allowed_mimetypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']

    file_mime_type = magic.from_buffer(image.read(), mime=True)
    if file_mime_type not in allowed_mimetypes:
        raise ValueError('Invalid image mimetype')
