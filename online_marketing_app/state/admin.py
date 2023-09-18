"""This module defines class StateModelAdmin"""
from django.contrib import admin
from state.models import State


class StateModelAdmin(admin.ModelAdmin):
    """This class configures the StateModelAdmin."""
    search_fields = ('id', 'name')
    ordering = ('created_at',)
    list_filter = ('name',)
    list_display = ('id', 'name')
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',),
        }),
    )

admin.site.register(State, StateModelAdmin)
