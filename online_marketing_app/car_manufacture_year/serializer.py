"""This module defines class ManufactureYearSerializer."""
from rest_framework import serializers
from car_manufacture_year.models import ManufactureYear


class ManufactureYearSerializer(serializers.ModelSerializer):
    """This class converts Django's queryset or object to a dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = ManufactureYear
        fields = '__all__'
