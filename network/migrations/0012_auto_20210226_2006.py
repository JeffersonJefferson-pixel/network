# Generated by Django 3.1.5 on 2021-02-26 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20210221_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='num_follower',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='num_following',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
