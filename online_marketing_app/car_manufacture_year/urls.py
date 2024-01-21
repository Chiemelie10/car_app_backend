"""This module defines all the endpoints relating to the Car model."""
from django.urls import path
from car_manufacture_year.views.get_manufacture_years import GetManufactureYears


urlpatterns = [
    path('api/years/', GetManufactureYears.as_view(), name='get-years'),
    # path('api/years', GetManufactureYears.as_view(), name='get-years'),
]
