# Generated by Django 3.2.18 on 2023-04-20 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drugs', '0004_alter_xmlsitemap_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='sitemap',
        ),
        migrations.AddField(
            model_name='provider',
            name='excluded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='provider',
            name='robots',
            field=models.URLField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='xmlsitemap',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sitemap', to='drugs.provider'),
        ),
    ]