# Generated by Django 5.1.3 on 2024-11-05 20:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Notifications', '0001_initial'),
        ('Routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trafficnotification',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Routes.route'),
        ),
    ]
