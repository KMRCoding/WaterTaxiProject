# Generated by Django 5.0.4 on 2024-04-13 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_emergency'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_class',
            field=models.CharField(choices=[('economy', 'Economy'), ('premium', 'Premium')], default='economy', max_length=20),
            preserve_default=False,
        ),
    ]
