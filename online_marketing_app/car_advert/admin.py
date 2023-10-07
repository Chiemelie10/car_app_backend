"""This module defines class CarAdvertModelAdmin."""
from django import forms
from django.contrib import admin
from car_advert.models import CarAdvert
from image.models import Image


class CarAdvertAdminForm(forms.ModelForm):
    """
    Inherited Django's built in form to implement custom validation logic.
    """
    class Meta:
        """
        model: The name of the model in the form.
        fields: fields of the named model.
        """
        model = CarAdvert
        fields = '__all__'

    def clean(self):
        """
        This method in a Django form is responsible for validating and cleaning
        the form data before it is saved to the database.
        """
        cleaned_data = super().clean()
        brand = cleaned_data.get('brand')
        model = cleaned_data.get('model')
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')

        if brand and model:
            if model.brand != brand:
                raise forms.ValidationError('Provided car model must have a matching car brand.')

        if state and city:
            if city.state != state:
                raise forms.ValidationError('Provided city must have a matching state.')


class ImageInline(admin.TabularInline):
    """th"""
    model = Image
    #fields = ('image',)
    extra = 1
    exclude = ('advertisement_images',)
    readonly_fields = ('id',)
    # classes = ['collapse']


class CarAdvertModelAdmin(admin.ModelAdmin):
    """This class configures the CarAdvertModelAdmin."""
    inlines = [
        ImageInline,
    ]
    form = CarAdvertAdminForm
    search_fields = ('id', 'fuel_type')
    list_filter = ('is_active', 'year', 'fuel_type')
    ordering = ('created_at',)
    list_display = ('id', 'is_active', 'brand', 'model', 'year', 'user')
    fieldsets = (
        (None, {'fields': ('thumbnail', 'thumbnail_cloud')}),
        (None, {'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                           'model', 'year', 'user', 'state', 'city', 'is_active',
                           'is_cloud_server_images', 'is_cloud_server_thumbnail')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                       'model', 'year', 'user', 'state', 'city', 'is_active'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Overrode the CarAdvert save model to put data in the tag field."""
        year = obj.year.year
        brand_name = obj.brand.name
        model_name = obj.model.name
        state_name = obj.state.name
        city_name = obj.city.name
        user_name = obj.user.username
        fuel_type = obj.fuel_type
        obj.tag = f'{year}, {brand_name}, {model_name}, {fuel_type}, '\
                    f'{state_name}, {city_name}, {user_name}'

        return super().save_model(request, obj, form, change)

admin.site.register(CarAdvert, CarAdvertModelAdmin)
