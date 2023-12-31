# Generated by Django 4.1.13 on 2023-12-11 12:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Interface', '0003_data_file_field_data_is_active_alter_data_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='balance_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='data',
            name='date_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), blank=True, null=True, size=None),
        ),
    ]
