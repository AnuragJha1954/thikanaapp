# Generated by Django 4.2.5 on 2024-10-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_relationship_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pincode',
            field=models.CharField(choices=[('458441', 'Neemuch'), ('458220', 'Jawad'), ('458110', 'Manasa')], default='458441', max_length=6),
        ),
        migrations.AddField(
            model_name='customuser',
            name='plain_password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
