"""This module defines the models of the car app"""
from uuid import uuid4
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from car_app.custom_user_manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """This class overwrites the user model provided by Django"""
    id = models.CharField(default=uuid4, primary_key=True, unique=True,
                          editable=False, max_length=36)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11,
                                    validators=[MinLengthValidator(limit_value=11)])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_marketer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    team_manager = models.ForeignKey('self', null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='managed_users')
    manager_code = models.CharField(max_length=12, blank=True, null=True, editable=False)
    referral_code = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        """db_table: States the table name in the database."""
        db_table = 'users'

    def __str__(self):
        """Returns a string representation of an instance of the User class."""
        return f'{self.username} {self.id}'
