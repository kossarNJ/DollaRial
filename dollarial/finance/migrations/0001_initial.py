# Generated by Django 2.0.4 on 2018-08-04 13:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dollarial.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', dollarial.fields.PriceField(decimal_places=2, max_digits=12, verbose_name='Amount')),
                ('currency', dollarial.fields.CurrencyField(choices=[('D', 'Dollar'), ('R', 'Rial'), ('E', 'Euro')], max_length=1, verbose_name='Currency')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Date')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BankPayment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='finance.Transaction')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('finance.transaction',),
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='finance.Transaction')),
                ('final_amount', dollarial.fields.PriceField(decimal_places=2, max_digits=12, verbose_name='Final Amount')),
                ('final_currency', dollarial.fields.CurrencyField(choices=[('D', 'Dollar'), ('R', 'Rial'), ('E', 'Euro')], max_length=1, verbose_name='Final Currency')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('finance.transaction',),
        ),
        migrations.AddField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_finance.transaction_set+', to='contenttypes.ContentType'),
        ),
    ]
