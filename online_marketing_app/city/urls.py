"""This module defines all the endpoints relating to the City model."""
from django.urls import path
from city.views.get_cities import GetCities
from city.views.get_cities_by_state import CitiesByState


urlpatterns = [
    path('api/cities/', GetCities.as_view(), name='get-cities'),
#     path('api/cities', GetCities.as_view(), name='get-cities'),
    path('api/states/<int:state_id>/cities/', CitiesByState.as_view(),
         name='get-cities-by-state'),
#     path('api/states/<int:state_id>/cities', CitiesByState.as_view(),
#          name='get-cities-by-state'),
]
