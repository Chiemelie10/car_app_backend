"""This module defines class UserActivity."""
from django.db import models
from car_app.models import User


class UserActivity(models.Model):
    """The attributes defines the columns of the "user_activities" table."""
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    activity_details = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """db_table: Defines name of the table this model creates in the database."""
        db_table = 'user_activities'

    def __str__(self):
        """Returns a string representation of an instance of the class."""
        return f'{self.user}'
