# Generated by Django 5.1.7 on 2025-04-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_customuser_managers_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, help_text='Имя пользователя, может быть пустым', max_length=10),
        ),
    ]
