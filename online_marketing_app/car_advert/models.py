"""This module defines class CarAdvert."""
from uuid import uuid4
from django.db import models
from car_app.models import User
from car_brand.models import CarBrand
from car_model.models import CarModel
from car_manufacture_year.models import ManufactureYear
from state.models import State
from city.models import City


FUEL_TYPE_CHOICES = (
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('liquefied petroleum', 'Liquefied Petroleum'),
    ('CNG', 'Compressed Natural Gas'),
    ('ethanol', 'Ethanol'),
    ('bio-diesel', 'Bio-Diesel'),
)

class CarAdvert(models.Model):
    """This class defines the fields of the model"""
    id = models.CharField(default=uuid4, primary_key=True,
                          unique=True, editable=False, max_length=36)
    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=100, blank=True, null=True, editable=False)
    price = models.DecimalField(decimal_places=2, max_digits=13)
    thumbnail = models.ImageField(upload_to='thumbnail', null=True, blank=True, default='')
    thumbnail_cloud = models.CharField(max_length=200, null=True, blank=True, default='')
    fuel_type = models.CharField(choices=FUEL_TYPE_CHOICES, max_length=110)
    brand = models.ForeignKey(CarBrand, related_name='adverts', on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, related_name='adverts', on_delete=models.CASCADE)
    year = models.ForeignKey(ManufactureYear, related_name='adverts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='adverts', on_delete=models.CASCADE)
    state = models.ForeignKey(State, related_name='adverts', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='adverts', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_cloud_server_images = models.BooleanField(default=False)
    is_cloud_server_thumbnail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """db_table: Defines the name of the model in the database."""
        db_table = "car_adverts"

    def __str__(self):
        """Returns a string representation of an instance of the CarAdvert class."""
        return f'{self.id}'
