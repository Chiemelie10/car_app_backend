"""This module defines class ImageModelAdmin"""
from django.contrib import admin
from image.models import Image


class ImageModelAdmin(admin.ModelAdmin):
    """This class configures the ImageModelAdmin."""
    pass

admin.site.register(Image, ImageModelAdmin)
