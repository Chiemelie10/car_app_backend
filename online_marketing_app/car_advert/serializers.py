"""This module defines the class CarAdvertSerializer."""
from rest_framework import serializers
from car_advert.models import CarAdvert
from image.serializers import ImageModelSerializer


class CarAdvertSerializer(serializers.ModelSerializer):
    """This class serializes the fields of class CarAdvert."""
    images = ImageModelSerializer(many=True, read_only=True)
    uploaded_images =serializers.ListField(
        required = False,
        child = serializers.ImageField(max_length=500, use_url=False),
        write_only = True
    )
    uploaded_cloud_images =serializers.ListField(
        required = False,
        child = serializers.CharField(max_length=500),
        write_only = True
    )
    is_active = serializers.BooleanField(default=True)
    thumbnail = serializers.FileField(required=False)
    thumbnail_cloud = serializers.CharField(required=False)
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = CarAdvert
        fields = '__all__'

    def to_representation(self, instance):
        """This method defines fields returned by the serializer"""
        if not instance.thumbnail or instance.thumbnail == '':
            representation = super().to_representation(instance)
            representation.pop('thumbnail', None)
        elif not instance.thumbnail_cloud or instance.thumbnail_cloud == '':
            representation = super().to_representation(instance)
            representation.pop('thumbnail_cloud', None)

        return representation
