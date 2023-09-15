"""This module defines class CarModelAdmin"""
from django.contrib import admin
from car_model.models import CarModel


class CarModelAdmin(admin.ModelAdmin):
    """This class configures the CarModelAdmin."""
    pass

admin.site.register(CarModel, CarModelAdmin)
