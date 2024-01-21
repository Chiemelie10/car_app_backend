"""This module defines the module SearchAdverts."""
from rest_framework.views import APIView
from django.http import JsonResponse
from car_advert.models import CarAdvert
from car_advert.serializers import CarAdvertSerializer
from car_advert.utils import paginate_queryset
from drf_spectacular.utils import extend_schema


class SearchAdvert(APIView):
    """This class defines a post method that searches for adverts."""
    # pylint: disable=no-member

    # serializer_class = CarAdvertSerializer

    @extend_schema(
        request={"application/json": {"example":
                                      {"search": "query string",
                                       "page": 1,
                                       "page_size": 1}}},
        responses={200: {"example": {'total_adverts': 1,
                                     'total_pages': 1,
                                     'previous_page': None,
                                     'next_page': None,
                                     'adverts': [
                                        {
                                            "id": "string",
                                            "images": [
                                                {
                                                "id": 0,
                                                "image": "string",
                                                "cloud_image": "string",
                                                "created_at": "2024-01-19T23:54:33.649Z",
                                                "updated_at": "2024-01-19T23:54:33.649Z",
                                                "car_advert": "string"
                                                }
                                            ],
                                            "is_active": True,
                                            "thumbnail": "string",
                                            "thumbnail_cloud": "string",
                                            "title": "string",
                                            "description": "string",
                                            "tag": "string",
                                            "price": "-639297.",
                                            "fuel_type": "petrol",
                                            "is_cloud_server_images": True,
                                            "is_cloud_server_thumbnail": True,
                                            "created_at": "2024-01-19T23:54:33.650Z",
                                            "updated_at": "2024-01-19T23:54:33.650Z",
                                            "brand": 0,
                                            "model": 0,
                                            "year": 0,
                                            "user": "string",
                                            "state": 0,
                                            "city": 0
                                        }
                                    ]
                                    }}},
    )
    def post(self, request):
        """This method searches for adverts by title, description, fuel_type or tag."""
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

        results = CarAdvert.objects.filter(is_active=True).raw(
            'SELECT * FROM car_adverts WHERE MATCH (title, description, tag) '\
            'AGAINST (%s)',[search_query]
        )

        result = paginate_queryset(results, page, page_size)

        if isinstance(result, JsonResponse):
            return result

        paginated_data, total_pages = result
        serializer = CarAdvertSerializer(paginated_data, many=True)

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
