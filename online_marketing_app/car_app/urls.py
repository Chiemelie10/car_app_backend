"""This module lists the different url routes available in the application."""
from django.urls import path
from car_app.views.register_marketer import MarketerRegistrationView


urlpatterns = [
    path('api/register/marketer/', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
    path('api/register/marketer', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
]
