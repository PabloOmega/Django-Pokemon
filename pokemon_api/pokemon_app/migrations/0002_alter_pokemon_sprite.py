# Generated by Django 4.2.7 on 2023-11-14 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemon",
            name="sprite",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
