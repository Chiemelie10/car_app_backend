"""This module defines class ImageModelSerializer."""
from rest_framework import serializers
from image.models import Image


class ImageModelSerializer(serializers.ModelSerializer):
    """This class converts django's queryset or object to dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = Image
        fields = '__all__'
