# Generated by Django 5.1 on 2024-11-16 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_datphong_so_khach'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datphong',
            old_name='chu_the',
            new_name='ngan_hang',
        ),
    ]
