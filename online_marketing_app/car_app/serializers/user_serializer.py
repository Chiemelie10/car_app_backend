"""This module defines class UserSerializer."""
from bs4 import BeautifulSoup
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from car_app.models import User


def validate_no_html_tags(field_value):
    """
    This function raises validation error if html tags are
    present in a string.
    """
    soup = BeautifulSoup(field_value, 'html.parser')
    if soup.find_all():
        raise ValidationError('HTML tags are not allowed.')

class UserModelSerializer(serializers.ModelSerializer):
    """This class validates the fields of the User model."""
    username = serializers.CharField(required=True, validators=[validate_no_html_tags])
    email = serializers.EmailField(required=True, validators=[validate_no_html_tags])
    password = serializers.CharField(required=True, min_length=8,
                                     validators=[validate_no_html_tags])

    class Meta:
        """Defines the model and fields to be validated."""
        model = User
        fields = '__all__'