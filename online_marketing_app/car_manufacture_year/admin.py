"""This module defines class ManufactureYearModelAdmin"""
from django.contrib import admin
from car_manufacture_year.models import ManufactureYear


class ManufactureYearModelAdmin(admin.ModelAdmin):
    """This class configures the ManufactureYearModelAdmin."""
    pass

admin.site.register(ManufactureYear, ManufactureYearModelAdmin)
