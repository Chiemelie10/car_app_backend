"""This module lists the different url routes available in the application."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from car_app.views.register_marketer import MarketerRegistrationView
from car_app.views.login_user import UserLogin
from car_app.views.logout_user import UserLogout
from car_app.views.get_delete_update_user import GetDeleteUpdateUser
from car_app.views.get_users import GetUsers
from car_app.views.get_user_adverts import GetUserAdverts
from car_app.views.get_user_advert import GetUserAdvert
from car_app.views.email_verification import VerifyEmail
from car_app.views.email_verification import SendEmailVerificationLink


urlpatterns = [
    path('api/register-marketer/', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
    path('api/register-marketer', MarketerRegistrationView.as_view(),
         name='marketer_registration'),
    path('api/login/', UserLogin.as_view(), name='login_user'),
    path('api/login', UserLogin.as_view(), name='login_user'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', UserLogout.as_view(), name='logout_user'),
    path('api/logout', UserLogout.as_view(), name='logout_user'),
    path('api/users/', GetUsers.as_view(), name='get_users'),
    path('api/users', GetUsers.as_view(), name='get_users'),
    path('api/users/<str:pk>/', GetDeleteUpdateUser.as_view(), name='get_delete_update_user'),
    path('api/users/<str:pk>', GetDeleteUpdateUser.as_view(), name='get_delete_update_user'),
    path('api/users/<str:user_id>/adverts/', GetUserAdverts.as_view(), name='get-user-adverts'),
    path('api/users/<str:user_id>/adverts', GetUserAdverts.as_view(), name='get-user-adverts'),
    path('api/users/<str:user_id>/adverts/<str:advert_id>', GetUserAdvert.as_view(),
         name='get-user-advert'),
    path('api/users/<str:user_id>/adverts/<str:advert_id>', GetUserAdvert.as_view(),
         name='get-user-advert'),
    path('api/verify-email/', VerifyEmail.as_view(), name='email_verify'),
    path('api/verify-email', VerifyEmail.as_view(), name='email_verify'),
    path('api/send-email', SendEmailVerificationLink.as_view(), name='send_email_link'),
    path('api/send-email', SendEmailVerificationLink.as_view(), name='send_email-link'),
]
