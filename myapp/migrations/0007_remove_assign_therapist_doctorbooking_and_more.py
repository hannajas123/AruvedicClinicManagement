# Generated by Django 4.0.1 on 2024-04-06 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_booking_total_remove_servicebooking_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assign_therapist',
            name='DOCTORBOOKING',
        ),
        migrations.AddField(
            model_name='assign_therapist',
            name='APPOINTMENT',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.appointment'),
            preserve_default=False,
        ),
    ]
