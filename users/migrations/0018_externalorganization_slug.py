# Generated by Django 5.1.7 on 2025-04-24 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_customuser_organizations'),
    ]

    operations = [
        migrations.AddField(
            model_name='externalorganization',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Slug организации'),
        ),
    ]
