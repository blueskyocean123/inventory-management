# Generated by Django 3.0.7 on 2021-09-06 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0002_auto_20201204_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellproduct',
            name='status',
        ),
        migrations.RemoveField(
            model_name='sellproduct',
            name='warehouse',
        ),
    ]
