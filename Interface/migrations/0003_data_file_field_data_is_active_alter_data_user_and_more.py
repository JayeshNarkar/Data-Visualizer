# Generated by Django 4.1.13 on 2023-12-11 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Interface', '0002_user_profile_picture_user_user_info_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='file_field',
            field=models.FileField(blank=True, null=True, upload_to='static/csv_files/'),
        ),
        migrations.AddField(
            model_name='data',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='data',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_pics/'),
        ),
    ]
