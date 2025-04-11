# Generated by Django 5.1.7 on 2025-04-11 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default=94334343, help_text='Номер телефона пользователя', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
