# Generated by Django 5.1.1 on 2024-10-18 13:45

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0004_transaction_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12),
        ),
    ]
