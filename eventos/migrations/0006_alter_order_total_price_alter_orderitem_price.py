# Generated by Django 5.1.3 on 2024-12-17 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_event_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(),
        ),
    ]
