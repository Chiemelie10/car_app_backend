"""This module defines the class CarAdvertSerializer."""
from rest_framework import serializers
from car_advert.models import CarAdvert
from image.serializers import ImageModelSerializer


class CarAdvertSerializer(serializers.ModelSerializer):
    """This class serializes the fields of class CarAdvert."""
    images = ImageModelSerializer(many=True, read_only=True)
    uploaded_images =serializers.ListField(
        child = serializers.ImageField(max_length=500, use_url=False),
        write_only = True
    )
    is_active = serializers.BooleanField(default=True)
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = CarAdvert
        fields = '__all__'
