from django.db import models

# Aquí se crean las tablas principales correspondientes a los datos de cada Pokemon, Habilidades y formas, para mayor información diríjase a la documentación de la API
# La Pokebase tiene una gran cantidad de información acerca de un pokemon, por lo que únicamente se carga una poca información por cuestiones de tiempo
class PokemonFormSprites(models.Model):
    # https://pokeapi.co/docs/v2#pokemonformsprites
    front_default = models.CharField(max_length=255, null=True)
    front_shiny = models.CharField(max_length=255, null=True)
    back_default = models.CharField(max_length=255, null=True)
    back_shiny = models.CharField(max_length=255, null=True)

class PokemonForm(models.Model):
    # https://pokeapi.co/docs/v2#pokemon-forms
    name = models.CharField(max_length=255)
    order = models.IntegerField(null=True)
    form_order = models.IntegerField(null=True)
    is_default = models.BooleanField(null=True)
    is_battle_only = models.BooleanField(null=True)
    is_mega = models.BooleanField(null=True)
    form_name = models.CharField(max_length=255, null=True)
    sprites = models.ForeignKey(PokemonFormSprites, on_delete=models.CASCADE, null=True)

class PokemonSprites(models.Model):
    # https://pokeapi.co/docs/v2#pokemonsprites
    front_default = models.CharField(max_length=255, null=True)
    front_shiny = models.CharField(max_length=255, null=True)
    front_female = models.CharField(max_length=255, null=True)
    front_shiny_female = models.CharField(max_length=255, null=True)
    back_default = models.CharField(max_length=255, null=True)
    back_shiny = models.CharField(max_length=255, null=True)
    back_female = models.CharField(max_length=255, null=True)
    back_shiny_female = models.CharField(max_length=255, null=True)

class Ability(models.Model):
    # https://pokeapi.co/docs/v2#abilities
    name = models.CharField(max_length=255)
    is_main_series = models.BooleanField(null=True)
    
    def __str__(self):
        return self.name 

class PokemonAbility(models.Model):
    # https://pokeapi.co/docs/v2#pokemonability
    is_hidden = models.BooleanField(null=True)
    slot = models.PositiveIntegerField(null=True)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, null=True)

class Pokemon(models.Model):
    # https://pokeapi.co/docs/v2#pokemon
    name = models.CharField(max_length=255)
    sprite = models.CharField(max_length=255,null=True)
    num_abilities = models.PositiveIntegerField(default=0)
    url_pokemon = models.URLField(null=True)
    
    base_experience = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    is_default = models.BooleanField(null=True)
    order = models.IntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)
    abilities = models.ManyToManyField(PokemonAbility)
    forms = models.ManyToManyField(PokemonForm)
    location_area_encounters = models.CharField(max_length=255, null=True) 
    sprites = models.ForeignKey(PokemonSprites, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name    
    