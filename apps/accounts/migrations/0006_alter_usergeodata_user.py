# Generated by Django 4.0.10 on 2023-05-21 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_usergeodata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergeodata',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_geo_data', to=settings.AUTH_USER_MODEL),
        ),
    ]
