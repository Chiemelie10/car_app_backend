"""This module defines class Brand"""
from django.db import models


class CarBrand(models.Model):
    """This class defines the fields of the model."""
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "car_brands"

    def __str__(self):
        """Returns a string representation of an instance of the CarBrand class."""
        return f'{self.name}'
