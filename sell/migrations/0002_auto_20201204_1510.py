# Generated by Django 3.0.7 on 2020-12-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellproduct',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='sellproduct',
            name='added_by',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
