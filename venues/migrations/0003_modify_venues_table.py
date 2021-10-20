# Generated by Django 2.2.9 on 2020-01-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("venues", "0002_add_translations_field"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="venue",
            name="seat_count",
        ),
        migrations.AddField(
            model_name="venuetranslation",
            name="accessibility_info",
            field=models.TextField(blank=True, verbose_name="accessibility info"),
        ),
        migrations.AddField(
            model_name="venuetranslation",
            name="additional_info",
            field=models.TextField(blank=True, verbose_name="additional info"),
        ),
        migrations.AddField(
            model_name="venuetranslation",
            name="address",
            field=models.CharField(blank=True, max_length=1000, verbose_name="address"),
        ),
        migrations.AddField(
            model_name="venuetranslation",
            name="arrival_instructions",
            field=models.TextField(blank=True, verbose_name="arrival instructions"),
        ),
        migrations.AddField(
            model_name="venuetranslation",
            name="www_url",
            field=models.URLField(blank=True, verbose_name="url"),
        ),
    ]
