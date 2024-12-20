# Generated by Django 5.1 on 2024-11-06 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_khachsan_slug_phong_slug_phong_trang_thai_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DanhGia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sao', models.IntegerField()),
                ('content', models.TextField()),
                ('thoi_gian', models.DateTimeField(auto_now_add=True)),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('phong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.phong')),
            ],
        ),
    ]