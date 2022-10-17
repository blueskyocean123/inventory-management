# Generated by Django 3.0.7 on 2021-09-06 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210906_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sell_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True),
        ),
    ]