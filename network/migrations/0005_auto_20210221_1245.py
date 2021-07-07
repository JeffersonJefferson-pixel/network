# Generated by Django 3.1.5 on 2021-02-21 05:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20210221_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='network.like'),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 2, 21, 12, 45, 29, 558022)),
        ),
    ]
