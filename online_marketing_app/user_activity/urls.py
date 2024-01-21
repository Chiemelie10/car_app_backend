"""This module defines the endpoints of the user_activity app."""
from rest_framework.urls import path
from user_activity.views.get_user_activities import GetUserActivity


urlpatterns = [
    # path('api/activities', GetUserActivity.as_view(), name='get-user-activity'),
    path('api/activities/', GetUserActivity.as_view(), name='get-user-activity'),
]
