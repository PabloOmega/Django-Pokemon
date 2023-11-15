import pokebase as pb
import requests

def get_pokemons():
    """
    Este método carga todos los nombres de pokemons existentes en la Base de Datos de la API
    """     
    pokemons = []
    
    try:
        for name in pb.APIResourceList("pokemon").names:    # Solo se utiliza el paquete Pokebase para cargar los nombres
            pokemons.append(name)
    except:
        print("Error de conexión")
        return None
    
    return pokemons

def get_abilities():
    """
    Este método carga todos los nombres de habilidades existentes en la Base de Datos de la API
    """       
    abilities = []
    
    try:
        for name in pb.APIResourceList("ability").names:
            abilities.append(name)
    except:
        print("Error de conexión")
        return None
    
    return abilities

def get_pokemon_forms():
    """
    Este método carga todos los nombres de formas de pokemons existentes en la Base de Datos de la API
    """     
    pokemon_forms = []
    
    try:
        for name in pb.APIResourceList("pokemon-form").names:
            pokemon_forms.append(name)
    except:
        print("Error de conexión")
        return None
    
    return pokemon_forms

def get_pokemons_data(pokemons_paged):
    """
    Este método carga la información de los pokemons a mostrarse en una determinada página o búsqueda
    """ 
    pokemons = []
    
    try:
        for pokemon_paged in pokemons_paged:
            # La carga se hace utilizando requests y no Pokebase, puesto que por alguna razón Pokebase se queda congelada
            pokemon = get_api("https://pokeapi.co/api/v2/pokemon/" + pokemon_paged.name)
            if not pokemon:
                return None
            
            #pokemon = pb.pokemon(pokemon_paged.name) # Esto sería con pokebase
            pokemons.append({
                "name": pokemon["name"],
                "sprite": pokemon["sprites"]["front_default"],
                "num_abilities": len(pokemon["abilities"]),
                "url_pokemon": ""
            })
    except:
        print("Error de conexión con la API de Pokemon")
        return None
    
    return pokemons   

def load_pokemon_data(pokemon):
    """
    Este método carga toda la información esperada en la página individual del pokemon
    """     
    try:
        pokemon_data = get_api("https://pokeapi.co/api/v2/pokemon/" + pokemon.name)
        if not pokemon_data:
            return None
            
        if not get_abilities_data(pokemon_data["abilities"]):   # Las habilidades no están incluidas en el mismo stream
            return None
        
        if not get_forms_data(pokemon_data["forms"]):   # Las formas no están incluidas en el mismo stream
            return None

        head = {  # Se crea una cabecera para identificar la información más importante facilmente
            "sprite": pokemon_data["sprites"]["front_default"],
            "num_abilities": len(pokemon_data["abilities"])
        }

        return {**head, **pokemon_data}
    
    except:
        print("Error de conexión")
        return None

def get_abilities_data(abilities_url):
    """
    Obtiene los datos de las habilidades y sobreescribe esta información en el mismo strem principal obtenido por la API
    """ 
    for i,ability_url in enumerate(abilities_url):
        ability = get_api(ability_url["ability"]["url"])
        
        if not ability:
            return None
        
        abilities_url[i]["ability"] = ability
        
    return "ok"

def get_forms_data(forms_url):
    """
    Obtiene los datos de las formas del pokemon y sobreescribe esta información en el mismo strem principal obtenido por la API
    """     
    for i,form_url in enumerate(forms_url):
        form = get_api(form_url["url"])
        
        if not form:
            return None
        
        forms_url[i] = form
        
    return "ok"

def get_api(api_url):
    """
    Este método permite comunicarse con la api de manera sencilla
    """     
    response = requests.get(api_url)
            
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        return None    
