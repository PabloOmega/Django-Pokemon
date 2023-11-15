from re import I
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from pokebase import ability
from .models import Pokemon, Ability, PokemonForm, PokemonAbility, PokemonFormSprites, PokemonSprites
from .pokemon_api import get_pokemons, get_abilities, get_pokemon_forms, get_pokemons_data, load_pokemon_data

# Create your views here.

def update_data():
    pokemons = get_pokemons()
    abilities = get_abilities()
    pokemon_forms = get_pokemon_forms()
    
    if pokemons:
        Pokemon.objects.all().delete()
        for pokemon in pokemons:
            Pokemon.objects.create(name=pokemon["name"], sprite=pokemon["sprite"], num_abilities=pokemon["num_abilities"])
            
    if abilities:
        Ability.objects.all().delete()
        for ability in abilities:
            Ability.objects.create(name=ability)
            
    if pokemon_forms:
        PokemonForm.objects.all().delete()
        for pokemon_form in pokemon_forms:
            PokemonForm.objects.create(name=pokemon_form)


def pokemon_list(request):
    query = request.GET.get('q')
    update = request.GET.get('a')
    page = request.GET.get('page')
    
    if update:
        update_data()

    if query:
        pokemons = Pokemon.objects.filter(name__icontains=query)
    else:
        pokemons = Pokemon.objects.all()
    
    paginator = Paginator(pokemons, 10)
    pokemons_paged = paginator.get_page(page)

    pokemons_paged_list = get_pokemons_data(pokemons_paged)
    if not pokemons_paged_list:
        raise Http404("No hay conexion con la API de Pokemon")
    
    update_data_page(pokemons_paged_list)

    pokemons_paged = paginator.get_page(page)

    return render(request, 'pokemon_list.html', {'pokemons': pokemons_paged, 'query': query})

def update_data_page(pokemons_paged):
    for pokemon in pokemons_paged:
        pokemon_instance = Pokemon.objects.get(name=pokemon["name"])
        Pokemon.objects.filter(id=pokemon_instance.id).update(sprite=pokemon["sprite"],num_abilities=pokemon["num_abilities"])
        
def pokemon_detail(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    
    pokemon_data = load_pokemon_data(pokemon)
    if not pokemon_data:
        raise Http404("No hay conexion con la API de Pokemon")
    
    pokemon.base_experience = pokemon_data["base_experience"]
    pokemon.height = pokemon_data["height"]
    pokemon.is_default = pokemon_data["is_default"]
    print(pokemon_data["order"],pokemon_data["order"])
    pokemon.order = pokemon_data["order"]
    pokemon.weight = pokemon_data["weight"]
    pokemon.location_area_encounters = pokemon_data["location_area_encounters"]  
    pokemon.save()
    
    pokemon.abilities.clear()
    update_data_abilities(pokemon_data["abilities"], pokemon)

    pokemon.forms.clear()
    update_pokemon_forms(pokemon_data["forms"], pokemon)
    
    create_sprites(pokemon_data["sprites"], pokemon)

    return render(request, 'pokemon_detail.html', {'pokemon': pokemon})

def update_data_abilities(pokemon_abilities, pokemon):
    for pokemon_ability in pokemon_abilities:
        ability = Ability.objects.get(name=pokemon_ability["ability"]["name"])
        ability.is_main_series = pokemon_ability["ability"]["is_main_series"]
        ability.save()
        pokemon_ability_instance = PokemonAbility.objects.create(
            is_hidden = pokemon_ability["is_hidden"],
            slot = pokemon_ability["slot"],
            ability = ability
        )
        pokemon.abilities.add(pokemon_ability_instance)
        
def update_pokemon_forms(pokemon_forms, pokemon):
    for pokemon_form in pokemon_forms:
        pokemon_form_sprites = PokemonFormSprites.objects.create(
            front_default = pokemon_form["sprites"]["front_default"],
            front_shiny = pokemon_form["sprites"]["front_shiny"],
            back_default = pokemon_form["sprites"]["back_default"],
            back_shiny = pokemon_form["sprites"]["back_shiny"]
        )
        pokemon_form_instance = PokemonForm.objects.get(name=pokemon_form["name"])
        pokemon_form_instance.name = pokemon_form["name"]
        pokemon_form_instance.order = pokemon_form["order"]
        pokemon_form_instance.form_order = pokemon_form["form_order"]
        pokemon_form_instance.is_default = pokemon_form["is_default"]
        pokemon_form_instance.is_battle_only = pokemon_form["is_battle_only"]
        pokemon_form_instance.is_mega = pokemon_form["is_mega"]
        pokemon_form_instance.form_name = pokemon_form["form_name"]
        pokemon_form_instance.sprites = pokemon_form_sprites
        pokemon_form_instance.save()
        pokemon.forms.add(pokemon_form_instance)
        
def create_sprites(pokemon_sprites, pokemon):
    pokemon_sprites_instance = PokemonSprites.objects.create(
        front_default = pokemon_sprites["front_default"],
        front_shiny = pokemon_sprites["front_shiny"],
        front_female = pokemon_sprites["front_female"],
        front_shiny_female = pokemon_sprites["front_shiny_female"],
        back_default = pokemon_sprites["back_default"],
        back_shiny = pokemon_sprites["back_shiny"],
        back_female = pokemon_sprites["back_female"],
        back_shiny_female = pokemon_sprites["back_shiny_female"]
    )
    pokemon.sprites = pokemon_sprites_instance
    pokemon.save()