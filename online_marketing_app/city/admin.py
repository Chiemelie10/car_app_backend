"""This module defines class CityModelAdmin"""
from django.contrib import admin
from city.models import City


class CityModelAdmin(admin.ModelAdmin):
    """This class configures the CityModelAdmin."""
    search_fields = ('id', 'name')
    ordering = ('created_at',)
    list_filter = ('name',)
    list_display = ('id', 'name', 'state')
    fieldsets = (
        (None, {'fields': ('name', 'state')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'state'),
        }),
    )

admin.site.register(City, CityModelAdmin)
