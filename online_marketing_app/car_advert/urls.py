"""This module defines all the endpoints relating to the CarAdvert module."""
from django.urls import path
from car_advert.views.get_adverts import GetAdverts
from car_advert.views.get_delete_update_advert import GetDeleteUpdateAdvert


urlpatterns = [
    path('api/adverts/', GetAdverts.as_view(), name='get-adverts'),
    path('api/adverts', GetAdverts.as_view(), name='get-adverts'),
    path('api/adverts/<str:pk>/', GetDeleteUpdateAdvert.as_view(),
         name='get-delete-update-adverts'),
    path('api/adverts/<str:pk>', GetDeleteUpdateAdvert.as_view(),
         name='get-delete-update-adverts'),
]
