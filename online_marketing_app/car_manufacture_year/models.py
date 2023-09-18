"""This module defines class ManufactureYear"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ManufactureYear(models.Model):
    """This class defines the fields of the model."""
    year = models.IntegerField(unique=True, validators=[
        MinValueValidator(limit_value=1970),
        MaxValueValidator(limit_value=9999)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "manufacture_years"

    def __str__(self):
        """Returns a string representation of an instance of the ManufactureYear class."""
        return f'{self.year}'
