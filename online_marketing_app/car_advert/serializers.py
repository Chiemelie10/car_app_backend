"""This module defines the class CarAdvertSerializer."""
from rest_framework import serializers
from car_advert.models import CarAdvert


class CarAdvertSerializer(serializers.ModelSerializer):
    """This class serializes the fields of class CarAdvert."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = CarAdvert
        fields = '__all__'
