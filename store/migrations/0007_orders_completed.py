# Generated by Django 4.1 on 2022-09-12 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
