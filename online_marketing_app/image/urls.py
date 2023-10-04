"""This module defines the endpoints for image app."""
from django.urls import path
from image.views.delete_image import DeleteImage


urlpatterns = [
    path('api/images/<int:image_id>/', DeleteImage.as_view(), name='delete-image'),
    path('api/images/<int:image_id>', DeleteImage.as_view(), name='delete-image'),
]
