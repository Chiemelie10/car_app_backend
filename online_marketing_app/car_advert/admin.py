"""This module defines class CarAdvertModelAdmin"""
from django.contrib import admin
from car_advert.models import CarAdvert
from image.models import Image


class ImageInline(admin.TabularInline):
    """th"""
    model = Image
    fields = ('image', 'is_thumbnail')
    extra = 1



class CarAdvertModelAdmin(admin.ModelAdmin):
    """This class configures the CarAdvertModelAdmin."""
    inlines = [
        ImageInline,
    ]
    search_fields = ('id', 'fuel_type')
    list_filter = ('is_active', 'year', 'fuel_type')
    ordering = ('created_at',)
    list_display = ('id', 'is_active', 'brand', 'model', 'year', 'user')
    
    fieldsets = (
        (None, {'fields': ('thumbnail',)}),
        (None, {'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                           'model', 'year', 'user', 'state', 'city', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                       'model', 'year', 'user', 'state', 'city', 'is_active'),
        }),
    )

admin.site.register(CarAdvert, CarAdvertModelAdmin)
