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

    def to_representation(self, instance):
        """This method defines fields returned when request method is GET or POST"""
        if not instance.image or instance.image == '':
            representation = super().to_representation(instance)
            representation.pop('image', None)
            representation.pop('created_at', None)
            representation.pop('updated_at', None)
        elif not instance.cloud_image or instance.cloud_image == '':
            representation = super().to_representation(instance)
            representation.pop('cloud_image', None)
            representation.pop('created_at', None)
            representation.pop('updated_at', None)

        return representation
