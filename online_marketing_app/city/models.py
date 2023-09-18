"""This module defines class City."""
from django.db import models
from state.models import State


class City(models.Model):
    """This class defines the fields of the model."""
    name = models.CharField(max_length=100, blank=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "cities"

    def __str__(self):
        """Returns a string representation of an instance of the City class."""
        return f'{self.name}'
