"""This module defines class CarBrandSerializer."""
from rest_framework import serializers
from car_brand.models import CarBrand


class CarBrandSerializer(serializers.ModelSerializer):
    """This class coverts Django's queryset or object to dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = CarBrand
        fields = '__all__'
