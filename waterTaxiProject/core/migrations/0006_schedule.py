# Generated by Django 5.0.4 on 2024-04-13 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ticket_trip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('route', models.CharField(choices=[('san_fernando_pos', 'San Fernando - POS'), ('pos_san_fernando', 'POS - San Fernando')], max_length=20)),
                ('departure_time', models.TimeField()),
                ('vessel', models.CharField(choices=[('carbo_star', 'Carbo Star')], max_length=50)),
            ],
        ),
    ]
