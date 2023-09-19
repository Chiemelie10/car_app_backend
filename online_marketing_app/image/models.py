"""This module defines class Image"""
from django.db import models
from car_advert.models import CarAdvert


class Image(models.Model):
    """This class defines the fields of the model."""
    car_advert = models.ForeignKey(CarAdvert, related_name='images',
                                      on_delete=models.CASCADE)
    image = models.ImageField(upload_to='advertisement_images', default='',
                              null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "images"

    def __str__(self):
        """Returns a string representation of an instance of the ManufactureYear class."""
        # pylint: disable=no-member
        return f'{self.id}'
