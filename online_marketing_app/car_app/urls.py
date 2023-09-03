"""This module lists the different url routes available in the application."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from car_app.views.register_marketer import MarketerRegistrationView
from car_app.views.login_user import UserLogin
from car_app.views.logout_user import UserLogout


urlpatterns = [
    path('api/register/marketer/', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
    path('api/register/marketer', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
    path('api/login/', UserLogin.as_view(), name='login_user'),
    path('api/login', UserLogin.as_view(), name='login_user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', UserLogout.as_view(), name='logout_user'),
    path('api/logout', UserLogout.as_view(), name='logout_user'),
]
