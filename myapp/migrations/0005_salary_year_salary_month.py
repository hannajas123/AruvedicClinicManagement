# Generated by Django 4.0.1 on 2024-04-06 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_therapist_qualification'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='Year',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salary',
            name='month',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]