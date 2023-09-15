"""This module defines class CityModelAdmin"""
from django.contrib import admin
from city.models import City


class CityModelAdmin(admin.ModelAdmin):
    """This class configures the CityModelAdmin."""
    pass

admin.site.register(City, CityModelAdmin)
