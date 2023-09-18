"""This module defines class CarModelSerializer."""
from rest_framework import serializers
from car_model.models import CarModel


class CarModelSerializer(serializers.ModelSerializer):
    """This class coverts Django's queryset or object to dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = CarModel
        fields = '__all__'
