"""This module defines class StateModelAdmin"""
from django.contrib import admin
from state.models import State


class StateModelAdmin(admin.ModelAdmin):
    """This class configures the StateModelAdmin."""
    pass

admin.site.register(State, StateModelAdmin)
