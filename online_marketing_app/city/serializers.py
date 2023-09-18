"""This module defines class CityModelSerializer."""
from rest_framework import serializers
from city.models import City


class CityModelSerializer(serializers.ModelSerializer):
    """This class coverts Django's queryset or object to dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = City
        fields = '__all__'
