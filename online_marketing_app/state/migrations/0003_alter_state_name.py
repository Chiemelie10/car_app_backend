# Generated by Django 4.2.5 on 2023-09-18 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0002_state_created_at_state_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
