"""This module defines class CarModel."""
from django.db import models
from car_brand.models import CarBrand


class CarModel(models.Model):
    """This class defines the fields of the model."""
    name = models.CharField(max_length=100, blank=False)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="brand_models")

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "car_models"

    def __str__(self):
        """Returns a string representation of an instance of the CarModel class."""
        return f'{self.name}'
