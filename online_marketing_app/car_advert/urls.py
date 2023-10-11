"""This module defines all the endpoints relating to the CarAdvert model."""
from django.urls import path
from car_advert.views.get_active_adverts import GetActiveAdverts
from car_advert.views.get_delete_update_advert import GetDeleteUpdateAdvert
from car_advert.views.get_adverts_by_brand import AdvertsByBrand
from car_advert.views.get_adverts_by_model import AdvertsByModel
from car_advert.views.get_adverts_by_manufacture_year import AdvertsByManufactureYear
from car_advert.views.get_adverts_by_state import AdvertsByState
from car_advert.views.get_images_by_advert import ImagesByAdvert
from car_advert.views.post_advert import PostAdvert
from car_advert.views.search import SearchAdvert
from car_advert.views.get_adverts_by_manager import GetManagerAdvert
from car_advert.views.get_adverts import GetAdverts


urlpatterns = [
    path('api/adverts/', GetActiveAdverts.as_view(), name='get-active-adverts'),
    path('api/adverts', GetActiveAdverts.as_view(), name='get-active-adverts'),
    path('api/all-adverts/', GetAdverts.as_view(), name='get-adverts'),
    path('api/all-adverts', GetAdverts.as_view(), name='get-adverts'),
    path('api/create-advert/', PostAdvert.as_view(), name='post-advert'),
    path('api/create-advert', PostAdvert.as_view(), name='post-advert'),
    path('api/search/', SearchAdvert.as_view(), name='search-advert'),
    path('api/search', SearchAdvert.as_view(), name='search-advert'),
    path('api/managers/<str:manager_id>/adverts/', GetManagerAdvert.as_view(),
         name='get-manager-adverts'),
    path('api/managers/<str:manager_id/adverts', GetManagerAdvert.as_view(),
         name='get-manager-adverts'),
    path('api/adverts/<str:pk>/', GetDeleteUpdateAdvert.as_view(),
         name='get-delete-update-adverts'),
    path('api/adverts/<str:pk>', GetDeleteUpdateAdvert.as_view(),
         name='get-delete-update-adverts'),
    path('api/adverts/brands/<int:brand_id>/', AdvertsByBrand.as_view(),
         name='adverts-by-brand'),
    path('api/adverts/brands/<int:brand_id>', AdvertsByBrand.as_view(),
         name='adverts-by-brand'),
    path('api/adverts/models/<int:model_id>/', AdvertsByModel.as_view(),
         name='adverts-by-model'),
    path('api/adverts/models/<int:model_id>', AdvertsByModel.as_view(),
         name='adverts-by-model'),
    path('api/adverts/years/<int:year_id>/', AdvertsByManufactureYear.as_view(),
         name='adverts-by-year'),
    path('api/adverts/years/<int:year_id>', AdvertsByManufactureYear.as_view(),
         name='adverts-by-year'),
    path('api/adverts/states/<int:state_id>/', AdvertsByState.as_view(),
         name='adverts-by-state'),
    path('api/adverts/states<int:state_id>', AdvertsByState.as_view(),
         name='adverts-by-state'),
    path('api/adverts/<str:advert_id>/images/', ImagesByAdvert.as_view(),
         name='images-by-advert'),
    path('api/adverts/<str:advert_id>/images', ImagesByAdvert.as_view(),
         name='images-by-advert'),
]
