"""This defines class UserAdminConfig."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from car_app.models import User
from car_app.utils import generate_ref_code


class UserAdminConfig(UserAdmin):
    """This class configures the admin webpage."""
    search_fields = ('id', 'username', 'email', 'referral_code')
    list_filter = ('is_active', 'is_verified', 'is_staff',
                   'is_marketer', 'is_manager', 'is_superuser')
    ordering = ('created_at',)
    list_display = ('id', 'username', 'is_verified', 'manager_code',
                    'referral_code', 'team_manager')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'team_manager')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_marketer',
                                    'is_superuser', 'is_verified', 'is_manager')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_manager', 'is_verified',
                       'is_superuser', 'is_marketer', 'referral_code'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Overrode this method to make the team_manager field to show only users
        that are managers.
        """
        if db_field.name == 'team_manager':
            kwargs['queryset'] = User.objects.filter(is_manager=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

        if change:
            user = User.objects.get(pk=obj.pk)
            prev_is_manager_value = user.is_manager
            prev_team_manager_value = user.team_manager

            if prev_is_manager_value is True and not obj.is_manager:
                obj.manager_code = None
                obj.is_staff = False
                managed_users = User.objects.filter(team_manager=obj)

                for managed_user in managed_users:
                    managed_user.team_manager = None
                    managed_user.referral_code = None
                    managed_user.save()
            if prev_is_manager_value is False and obj.is_manager:
                code = generate_ref_code()
                obj.manager_code = code
                obj.is_staff = True
                obj.team_manager = None

            if not prev_team_manager_value and obj.team_manager:
                new_manager = obj.team_manager
                is_superuser = new_manager.is_superuser
                if is_superuser:
                    obj.referral_code = None
                elif new_manager:
                    manager_code = new_manager.manager_code
                    obj.referral_code = manager_code

            if prev_team_manager_value and not obj.team_manager:
                obj.referral_code = None

            if prev_team_manager_value and obj.team_manager != prev_team_manager_value:
                new_manager = obj.team_manager
                if new_manager:
                    is_superuser = new_manager.is_superuser
                    if is_superuser:
                        obj.referral_code = None
                    else:
                        manager_code = new_manager.manager_code
                        obj.referral_code = manager_code


        referral_code = form.cleaned_data.get('referral_code')

        if referral_code:
            try:
                manager = User.objects.get(manager_code=referral_code)
                obj.team_manager = manager
            except User.DoesNotExist: # pylint: disable=no-member
                pass

        return super().save_model(request, obj, form, change)

admin.site.register(User, UserAdminConfig)
