"""This module defines all the endpoints relating to the CarBrand model."""
from django.urls import path
from car_brand.views.get_brands import GetBrands


urlpatterns = [
    path('api/brands/', GetBrands.as_view(), name='get-brands'),
    path('api/brands', GetBrands.as_view(), name='get-brands'),
]
