# Generated by Django 5.1.3 on 2024-11-18 23:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_category_remove_event_category_event_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Lugar')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.OneToOneField(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='eventos.location', verbose_name='Lugar'),
        ),
    ]