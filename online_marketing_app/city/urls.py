"""This module defines all the endpoints relating to the City model."""
from django.urls import path
from city.views.get_cities import GetCities


urlpatterns = [
    path('api/cities/', GetCities.as_view(), name='get-cities'),
    path('api/cities', GetCities.as_view(), name='get-cities'),
]
