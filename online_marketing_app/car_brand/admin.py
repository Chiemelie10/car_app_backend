"""This module defines class CarBrandModelAdmin"""
from django.contrib import admin
from car_brand.models import CarBrand


class CarBrandModelAdmin(admin.ModelAdmin):
    """This class configures the CarAdvertModelAdmin."""
    pass

admin.site.register(CarBrand, CarBrandModelAdmin)
