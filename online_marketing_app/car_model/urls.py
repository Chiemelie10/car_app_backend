"""This module defines all the endpoints relating to the CarModel model."""
from django.urls import path
from car_model.views.get_models import GetModels
from car_model.views.get_models_by_brand import ModelsByBrand


urlpatterns = [
    path('api/models/', GetModels.as_view(), name='get-models'),
    path('api/models', GetModels.as_view(), name='get-models'),
    path('api/brands/<int:brand_id>/models/', ModelsByBrand.as_view(),
         name='get-models-by-brand'),
    path('api/brands/<int:brand_id>/models', ModelsByBrand.as_view(),
         name='get-models-by-brand'),
]
