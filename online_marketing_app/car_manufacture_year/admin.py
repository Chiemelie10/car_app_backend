"""This module defines class ManufactureYearModelAdmin"""
from django.contrib import admin
from car_manufacture_year.models import ManufactureYear


class ManufactureYearModelAdmin(admin.ModelAdmin):
    """This class configures the ManufactureYearModelAdmin."""
    search_fields = ('id', 'year')
    ordering = ('created_at',)
    list_filter = ('year',)
    list_display = ('id', 'year')
    fieldsets = (
        (None, {'fields': ('year',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('year',),
        }),
    )

admin.site.register(ManufactureYear, ManufactureYearModelAdmin)
