"""This class defines class UserActivitySerializer."""
from rest_framework import serializers
from user_activity.models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    """Defines the fields of the class that will be serialized"""
    class Meta:
        """
        model: Defines name of the model to be serialized.
        fields: Defines fields of the model that will be serialized.
        """
        model = UserActivity
        fields = '__all__'
