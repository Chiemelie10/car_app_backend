"""This module defines class CarBrandModelAdmin"""
from django.contrib import admin
from car_brand.models import CarBrand


class CarBrandModelAdmin(admin.ModelAdmin):
    """This class configures the CarAdvertModelAdmin."""
    search_fields = ('id', 'name')
    ordering = ('created_at',)
    list_filter = ('name',)
    list_display = ('id', 'name')
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',),
        }),
    )

admin.site.register(CarBrand, CarBrandModelAdmin)
