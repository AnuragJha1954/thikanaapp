# Generated by Django 4.2.5 on 2024-10-24 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='photo',
        ),
    ]