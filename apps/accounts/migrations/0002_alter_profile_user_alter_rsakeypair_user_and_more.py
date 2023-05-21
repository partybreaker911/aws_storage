# Generated by Django 4.0.10 on 2023-05-21 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rsakeypair',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rsa_key_pair', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usergeodata',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_geo_data', to=settings.AUTH_USER_MODEL),
        ),
    ]
