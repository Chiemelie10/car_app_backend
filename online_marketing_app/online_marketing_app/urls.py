"""
URL configuration for online_marketing_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pylint: disable=unused-import
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from car_app.views.exception_handlers.page_not_found import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('car_app.urls')),
    path('', include('car_advert.urls')),
    path('', include('user_activity.urls')),
    path('', include('state.urls')),
    path('', include('city.urls')),
    path('', include('car_model.urls')),
    path('', include('car_manufacture_year.urls')),
    path('', include('car_brand.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'CarAutosNG'

# pylint: disable=invalid-name
handler404 = 'car_app.views.exception_handlers.page_not_found.custom_404_view'
