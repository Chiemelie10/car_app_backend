"""This module defines all the endpoints relating to the State model."""
from django.urls import path
from state.views.get_states import GetStates


urlpatterns = [
    path('api/states/', GetStates.as_view(), name='get-states'),
    # path('api/states', GetStates.as_view(), name='get-states'),
]
