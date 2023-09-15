"""This module defines all the endpoints relating to the CarAdvert module."""
from django.urls import path
from car_advert.views.get_adverts import GetAdverts


urlpatterns = [
    path('api/adverts/', GetAdverts.as_view(), name='get-adverts'),
    path('api/adverts', GetAdverts.as_view(), name='get-adverts')
]
