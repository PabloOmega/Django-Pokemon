from re import I
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404
from pokebase import ability
from .models import Pokemon, Ability, PokemonForm, PokemonAbility, PokemonFormSprites, PokemonSprites
from .pokemon_api import get_pokemons, get_abilities, get_pokemon_forms, get_pokemons_data, load_pokemon_data

# Create your views here.

def update_data():
    """
    Reserva un espacio en la base de datos para todos los pokemons cargando unicamente los nombres y creando un objeto 
    para cada nombre. Con get_pokemons() se llama a la API y devuelve una lista con los nombres.
    """
    pokemons = get_pokemons()
    # abilities = get_abilities()
    # pokemon_forms = get_pokemon_forms()
    
    if pokemons:
        Pokemon.objects.all().delete()  # Elimina todos los pokemons existentes para evitar duplicados
        for pokemon in pokemons:
            Pokemon.objects.create(name=pokemon)    # Crea un objeto o registro para cada pokemon
            
    # if abilities:
    #     Ability.objects.all().delete()
    #     for ability in abilities:
    #         Ability.objects.create(name=ability)
            
    # if pokemon_forms:
    #     PokemonForm.objects.all().delete()
    #     for pokemon_form in pokemon_forms:
    #         PokemonForm.objects.create(name=pokemon_form)


def pokemon_list(request):
    """
    Este método se llama cuando se carga la página principal. Se encarga de paginar los pokemones y filtrarlos en función de
    la búsqueda. Si no tiene pokemons se llama automáticamente a update_data para cargar todos los pokemons de la API.
    """    
    query = request.GET.get('q')    # Permite realizar la búsqueda
    update = request.GET.get('a')   # Si se envía el parámetro a, se eliminarán todos los pokemons para volverlos a cargar
    page = request.GET.get('page')  # Permite definir el número de página y los pokemons que se deben mostrar
    
    if update or not Pokemon.objects.all():
        update_data()   # Elimina todos los pokemons y los vuelve a cargar desde la API

    if query:
        pokemons = Pokemon.objects.filter(name__icontains=query)    # Filtra los pokemons en función de la búsqueda
    else:
        pokemons = Pokemon.objects.all()    # Si no hay búsqueda, se devuelve todos los pokemons
    
    paginator = Paginator(pokemons, 10) # Paginación de los pokemons
    pokemons_paged = paginator.get_page(page)

    pokemons_paged_list = get_pokemons_data(pokemons_paged) # Envía los pokemons paginados para cargar sus datos y mostrarlos
    if not pokemons_paged_list:
        raise Http404("No hay conexion con la API de Pokemon")  # Si no se obtienen los datos, seguramente existe error con la API
    
    update_data_page(pokemons_paged_list)   # Actualiza en la base de datos con los datos cargados de la API

    pokemons_paged = paginator.get_page(page)   # Vuelve a paginar con los datos completos

    return render(request, 'pokemon_list.html', {'pokemons': pokemons_paged, 'query': query})

def update_data_page(pokemons_paged):
    """
    Actualiza la base de datos con los datos cargados de la API y únicamente los objetos que corresponden a la página mostrada
    """      
    for pokemon in pokemons_paged:
        pokemon_instance = Pokemon.objects.get(name=pokemon["name"])    # Carga el pokemon en función del nombre
        Pokemon.objects.filter(id=pokemon_instance.id).update(sprite=pokemon["sprite"],num_abilities=pokemon["num_abilities"])
        
def pokemon_detail(request, pokemon_id):
    """
    Este método se llama cuando se carga la página individual de cada pokemon. Se encarga de cargar todos los datos esperados
    por el Pokemon especificado en el "pokemon_id"
    """       
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id) # Carga el pokemon o muestra la página 404 si no lo encuentra
    
    pokemon_data = load_pokemon_data(pokemon)   # Carga desde la API todos los datos esperados por el pokemon
    if not pokemon_data:
        raise Http404("No hay conexion con la API de Pokemon")  # Si no se obtienen los datos, seguramente existe error con la API
    
    pokemon.base_experience = pokemon_data["base_experience"]
    pokemon.height = pokemon_data["height"]
    pokemon.is_default = pokemon_data["is_default"]
    pokemon.order = pokemon_data["order"]
    pokemon.weight = pokemon_data["weight"]
    pokemon.location_area_encounters = pokemon_data["location_area_encounters"]  
    pokemon.save()  # Guarda los datos obtenidos
    
    pokemon.abilities.clear()   # Cómo se vuelven a cargar las habilidades, se borran las relaciones para volver a relacionar
    update_data_abilities(pokemon_data["abilities"], pokemon)   # Actualiza en la base de datos las habilidades

    pokemon.forms.clear()   # Cómo se vuelven a cargar las habilidades, se borran las formas para volver a relacionar
    update_pokemon_forms(pokemon_data["forms"], pokemon)    # Actualiza en la base de datos las formas de pokemons
    
    create_sprites(pokemon_data["sprites"], pokemon)    # Carga en la base de datos los Sprites

    return render(request, 'pokemon_detail.html', {'pokemon': pokemon})

def update_data_abilities(pokemon_abilities, pokemon):
    """
    Este método actualiza las habilidades en la base de datos.
    """       
    for pokemon_ability in pokemon_abilities:
        # Como puede existir pokemons con la misma habilidad, se comprueba si ya está cargada la habilidad
        ability, _ = Ability.objects.get_or_create(name=pokemon_ability["ability"]["name"])
        ability.is_main_series = pokemon_ability["ability"]["is_main_series"]
        ability.save()
        # Se añade la habilidad del Pokemon, para más información diríjase a la documentación de la Pokemon API
        pokemon_ability_instance = PokemonAbility.objects.create(
            is_hidden = pokemon_ability["is_hidden"],
            slot = pokemon_ability["slot"],
            ability = ability
        )
        pokemon.abilities.add(pokemon_ability_instance)
        
def update_pokemon_forms(pokemon_forms, pokemon):
    """
    Este método actualiza las formas del pokemon en la base de datos.
    """       
    for pokemon_form in pokemon_forms:
        # Crea las formas que tiene pokemon
        pokemon_form_sprites = PokemonFormSprites.objects.create(
            front_default = pokemon_form["sprites"]["front_default"],
            front_shiny = pokemon_form["sprites"]["front_shiny"],
            back_default = pokemon_form["sprites"]["back_default"],
            back_shiny = pokemon_form["sprites"]["back_shiny"]
        )
        # Para evitar volver a añadir otra forma con el mismo nombre, se comprueba si ya existe para no crearla
        pokemon_form_instance, _ = PokemonForm.objects.get_or_create(name=pokemon_form["name"])
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
    """
    Este método crea los diferentes Sprites del pokemon en la base de datos
    """         
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