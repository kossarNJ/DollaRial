# Generated by Django 2.0.4 on 2018-08-04 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_auto_20180803_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]