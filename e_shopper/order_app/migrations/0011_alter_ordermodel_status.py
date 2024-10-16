# Generated by Django 4.2.6 on 2024-07-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0010_ordermodel_payment_status_ordermodel_shipping_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('received', 'Received'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=20),
        ),
    ]
