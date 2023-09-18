"""This module defines class CarAdvertModelAdmin"""
from django import forms
from django.contrib import admin
from car_advert.models import CarAdvert
from image.models import Image


# class CarAdvertAdminForm(forms.ModelForm):
#     class Meta:
#         model = CarAdvert
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['images'].widget = forms.ClearableFileInput(attrs={'multiple': True})


class ImageInline(admin.StackedInline):
    """th"""
    model = Image
    #fields = ('image',)
    extra = 0


class CarAdvertModelAdmin(admin.ModelAdmin):
    """This class configures the CarAdvertModelAdmin."""
    inlines = [
        ImageInline,
    ]
    search_fields = ('id', 'fuel_type')
    list_filter = ('is_active', 'year', 'fuel_type')
    ordering = ('created_at',)
    list_display = ('id', 'is_active', 'brand', 'model', 'year', 'user')
    fieldsets = (
        (None, {'fields': ('thumbnail',)}),
        (None, {'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                           'model', 'year', 'user', 'state', 'city', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'price', 'fuel_type', 'brand',
                       'model', 'year', 'user', 'state', 'city', 'is_active'),
        }),
    )

admin.site.register(CarAdvert, CarAdvertModelAdmin)
