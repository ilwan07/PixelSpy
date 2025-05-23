# Generated by Django 5.2.1 on 2025-05-24 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixelspy', '0003_tracker_request_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pixel',
            name='display_url',
            field=models.URLField(default=None, verbose_name='pixel display url'),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='request_header',
            field=models.CharField(default='', verbose_name='request header metadata'),
        ),
    ]
