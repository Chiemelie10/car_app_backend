"""This defines class UserAdminConfig."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from car_app.models import User
from car_app.utils import generate_ref_code

# Register your models here.
class UserAdminConfig(UserAdmin):
    """This class configures the admin webpage."""
    search_fields = ('id', 'username', 'email', 'manager_code')
    list_filter = ('username', 'email', 'is_active', 'is_verified', 'is_staff',
                   'is_marketer', 'is_manager', 'is_superuser')
    ordering = ('created_at',)
    list_display = ('id', 'username', 'email', 'is_active', 'is_verified',
                    'is_staff', 'is_marketer', 'is_manager', 'is_superuser',
                    'manager_code', 'team_manager')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'team_manager')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_marketer',
                                    'is_superuser', 'is_verified', 'is_manager')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active',
                       'is_staff', 'is_manager', 'is_verified', 'is_superuser',
                       'is_marketer', 'referral_code'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        The UserAdmin save_model was overrode to achieve the following
        when aing a new user through the Django admin web page:
        1) Generate unique codes called manager_code in the User model
        only when a manager level user is being registere.
        2) Establish a relationship between a marketer and a manager
        through the manager's unique code.
        """
        if obj.is_manager and not change:
            code = generate_ref_code()
            obj.manager_code = code

        referral_code = form.cleaned_data.get('referral_code')

        if referral_code:
            try:
                manager = User.objects.get(manager_code=referral_code)
                obj.team_manager = manager
            except User.DoesNotExist: # pylint: disable=no-member
                pass

        return super().save_model(request, obj, form, change)

admin.site.register(User, UserAdminConfig)
