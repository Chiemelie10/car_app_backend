"""This module defines class UserActivityAdmin"""
from django.contrib import admin
from user_activity.models import UserActivity


class UserActivityAdmin(admin.ModelAdmin):
    """This class configures the UserActivity model on the admin web page."""
    search_fields = ('id',)
    ordering = ('timestamp',)
    list_display = ('id', 'user', 'activity_type', 'activity_details', 'timestamp')


admin.site.register(UserActivity, UserActivityAdmin)
