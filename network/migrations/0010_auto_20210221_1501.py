# Generated by Django 3.1.5 on 2021-02-21 08:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20210221_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 2, 21, 15, 1, 2, 479702)),
        ),
    ]
