# Generated by Django 5.1 on 2024-11-15 15:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_tiennghi_khach_san_alter_khachsan_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='khuyenmai',
            name='ngay_ket_thuc',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='khuyenmai',
            name='phong',
            field=models.ManyToManyField(blank=True, related_name='khuyenmais', to='booking.phong'),
        ),
        migrations.AlterField(
            model_name='phong',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='phong',
            name='ten',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='tiennghi',
            name='khach_san',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.khachsan'),
        ),
        migrations.AlterField(
            model_name='tiennghi',
            name='ten',
            field=models.CharField(max_length=100),
        ),
    ]
