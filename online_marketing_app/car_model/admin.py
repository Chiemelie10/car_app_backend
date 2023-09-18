"""This module defines class CarModelAdmin"""
from django.contrib import admin
from car_model.models import CarModel


class CarModelAdmin(admin.ModelAdmin):
    """This class configures the CarModelAdmin."""
    search_fields = ('id', 'name')
    ordering = ('created_at',)
    list_filter = ('name',)
    list_display = ('id', 'name', 'brand')
    fieldsets = (
        (None, {'fields': ('name', 'brand')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'brand'),
        }),
    )


admin.site.register(CarModel, CarModelAdmin)
