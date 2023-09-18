"""This module defines all the endpoints relating to the CarModel model."""
from django.urls import path
from car_model.views.get_models import GetModels


urlpatterns = [
    path('api/models/', GetModels.as_view(), name='get-models'),
    path('api/models', GetModels.as_view(), name='get-models'),
]
