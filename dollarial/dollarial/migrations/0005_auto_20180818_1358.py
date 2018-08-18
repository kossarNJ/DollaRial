# Generated by Django 2.0.4 on 2018-08-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dollarial', '0004_auto_20180811_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='automatic_user',
            field=models.BooleanField(default=False, verbose_name='Automatically Created'),
        ),
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(max_length=64, verbose_name='Account Number'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('automatic_user', 'account_number')},
        ),
    ]