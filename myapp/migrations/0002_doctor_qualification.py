# Generated by Django 4.0.1 on 2024-04-05 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='qualification',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
