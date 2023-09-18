# Generated by Django 4.2.5 on 2023-09-18 04:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_manufacture_year', '0002_manufactureyear_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufactureyear',
            name='year',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(limit_value=1970), django.core.validators.MaxValueValidator(limit_value=9999)]),
        ),
    ]
