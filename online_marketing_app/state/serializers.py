"""This module defines class StateModelSerializer."""
from rest_framework import serializers
from state.models import State


class StateModelSerializer(serializers.ModelSerializer):
    """This class coverts Django's queryset or object to dictionary."""
    class Meta:
        """
        model: The name of the model that will be serialized.
        fields: Lists fields of the named model that will be serialized.
        """
        model = State
        fields = '__all__'
