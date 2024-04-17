# Generated by Django 5.0.4 on 2024-04-10 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.CharField(choices=[('san_fernando_pos', 'San Fernando - POS'), ('pos_san_fernando', 'POS - San Fernando')], max_length=100)),
                ('schedule_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('adult_passengers', models.IntegerField()),
                ('teenage_passengers', models.IntegerField()),
                ('infant_passengers', models.IntegerField()),
                ('elderly_passengers', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
