# Generated by Django 5.2.1 on 2025-06-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixelspy', '0007_rename_creation_date_pixel_date_pixel_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='date',
            field=models.DateTimeField(verbose_name='date of opening'),
        ),
    ]
