"""This module defines class ImageModelAdmin"""
from django.contrib import admin
from image.models import Image


class ImageModelAdmin(admin.ModelAdmin):
    """This class configures the ImageModelAdmin."""
    # search_fields = ('id', 'image')
    # ordering = ('created_at',)
    # list_filter = ('image',)
    # list_display = ('id', 'image', 'advertisement')
    # fieldsets = (
    #     (None, {'fields': ('image', 'advertisement')}),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('image', 'advertisement'),
    #     }),
    # )
    pass

admin.site.register(Image, ImageModelAdmin)
