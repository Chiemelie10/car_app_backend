# Generated by Django 4.2.5 on 2023-09-24 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car_advert', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('car_manufacture_year', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='caradvert',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adverts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='caradvert',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adverts', to='car_manufacture_year.manufactureyear'),
        ),
        migrations.RunSQL(
            sql= 'CREATE FULLTEXT INDEX car_advert_fulltext_idx ON car_adverts (title, tag, description);',
            reverse_sql='DROP INDEX car_advert_fulltext_idx ON car_adverts;'
        ),
    ]
