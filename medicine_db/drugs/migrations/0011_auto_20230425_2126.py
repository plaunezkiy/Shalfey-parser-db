# Generated by Django 3.2.18 on 2023-04-25 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0010_auto_20230425_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='providercategory',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]