import pokebase as pb
import requests

def get_pokemons():
    pokemons = []
    
    try:
        for name in pb.APIResourceList("pokemon").names:
            pokemons.append({
                "name": name,
                "sprite": "",
                "num_abilities": 0,
                "url_pokemon": ""
            })
    except:
        print("Error de conexión")
        return None
    
    return pokemons

def get_abilities():
    abilities = []
    
    try:
        for name in pb.APIResourceList("ability").names:
            abilities.append(name)
    except:
        print("Error de conexión")
        return None
    
    return abilities

def get_pokemon_forms():
    pokemon_forms = []
    
    try:
        for name in pb.APIResourceList("pokemon-form").names:
            pokemon_forms.append(name)
    except:
        print("Error de conexión")
        return None
    
    return pokemon_forms

def get_pokemons_data(pokemons_paged):
    pokemons = []
    
    try:
        for pokemon_paged in pokemons_paged:
            # api_url = "https://pokeapi.co/api/v2/pokemon/" + pokemon_paged.name
            # response = requests.get(api_url)
            
            # if response.status_code == 200:
            #     pokemon = response.json()
            # else:
            #     print(f"Error en la solicitud. Código de estado: {response.status_code}")
            #     return None
            pokemon = get_api("https://pokeapi.co/api/v2/pokemon/" + pokemon_paged.name)
            if not pokemon:
                return None
            
            #pokemon = pb.pokemon(pokemon_paged.name)
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
    try:
        # api_url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.name
        # response = requests.get(api_url)
            
        # if response.status_code == 200:
        #     pokemon_data = response.json()
        # else:
        #     print(f"Error en la solicitud. Código de estado: {response.status_code}")
        #     return None
        pokemon_data = get_api("https://pokeapi.co/api/v2/pokemon/" + pokemon.name)
        if not pokemon_data:
            return None
            
        if not get_abilities_data(pokemon_data["abilities"]):
            return None
        
        if not get_forms_data(pokemon_data["forms"]):
            return None

        head = {  
            "sprite": pokemon_data["sprites"]["front_default"],
            "num_abilities": len(pokemon_data["abilities"])
        }

        return {**head, **pokemon_data}
    
    except:
        print("Error de conexión")
        return None

def get_abilities_data(abilities_url):
    for i,ability_url in enumerate(abilities_url):
        ability = get_api(ability_url["ability"]["url"])
        
        if not ability:
            return None
        
        abilities_url[i]["ability"] = ability
        
    return "ok"

def get_forms_data(forms_url):
    for i,form_url in enumerate(forms_url):
        form = get_api(form_url["url"])
        
        if not form:
            return None
        
        forms_url[i] = form
        
    return "ok"

def get_api(api_url):
    response = requests.get(api_url)
            
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        return None    
