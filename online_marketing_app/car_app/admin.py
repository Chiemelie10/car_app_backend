"""This defines class UserAdminConfig."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from car_app.models import User

# Register your models here.
class UserAdminConfig(UserAdmin):
    """This class configures the admin webpage."""
    search_fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('created_at',)
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff',
                    'is_superuser', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_superuser'),
        }),
    )

admin.site.register(User, UserAdminConfig)
