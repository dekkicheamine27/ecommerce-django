# Generated by Django 4.1 on 2022-11-01 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        ('orders', '0003_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='store.variation'),
        ),
    ]
