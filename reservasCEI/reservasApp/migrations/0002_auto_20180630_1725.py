# Generated by Django 2.0.5 on 2018-06-30 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservasApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservaarticulo',
            name='fecha_reserva',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 30, 17, 25, 52, 353732)),
        ),
        migrations.AddField(
            model_name='reservaespacio',
            name='fecha_reserva',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 30, 17, 25, 52, 354240)),
        ),
    ]
