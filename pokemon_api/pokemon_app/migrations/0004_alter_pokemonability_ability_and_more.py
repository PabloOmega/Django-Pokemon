# Generated by Django 4.2.7 on 2023-11-14 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon_app", "0003_ability_pokemonformsprites_pokemonsprites_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemonability",
            name="ability",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="pokemon_app.ability",
            ),
        ),
        migrations.AlterField(
            model_name="pokemonform",
            name="form_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="pokemonform",
            name="sprites",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="pokemon_app.pokemonformsprites",
            ),
        ),
    ]