"""This module defines class ManufactureYear"""
from django.db import models


class ManufactureYear(models.Model):
    """This class defines the fields of the model."""
    year = models.IntegerField(unique=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "manufacture_years"

    def __str__(self):
        """Returns a string representation of an instance of the ManufactureYear class."""
        return f'{self.year}'
