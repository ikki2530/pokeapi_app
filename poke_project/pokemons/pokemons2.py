import requests
import copy
import re
import time


def get_evolution_data(list_names=[]):
    """
    Obtiene información de cada evolución del pokemon.
    Parametros:
    - list_names: lista de nombres de pokemons de la cadena de evolución
    Return:
    - list_evolutions: lista con información de los
    pokemons de la cadena de evolución (id, nombre, peso,
    altura, estadísticas base)
    """
    list_evolutions = []
    pokemon_info = {}
    if list_names:
        for name in list_names:
            url_pok = "https://pokeapi.co/api/v2/pokemon/"
            pokemon_info = request_pokemon(url_pok, name=name)
            list_evolutions.append(pokemon_info)
    return list_evolutions


def get_evolution_names(evols_list_dicts=[], names=[], cont=0):
    """
    Funcion recursiva para obtener los nombres de la cadena de evolución.
    Parametros:
    - evols_list_dicts: lista con la cadena de evolución del pokemon.
    - names: lista para almacenar los nombres de la cadena
    de evolución del pokemon.
    - cont: contador, para saber cada pokemon de quien evoluciona.
    Return:
    - names: lista con los nombres de los pokemons de la cadena de evolución.
    """
    lista_names = []

    if evols_list_dicts:
        for evols_dict in evols_list_dicts:
            next_evols_list = evols_dict.get("evolves_to", [])
            specie_dict = evols_dict.get("species", {})
            name = specie_dict.get("name", "")
            names.append(name + "_" + str(cont))

            if next_evols_list:
                cont += 1
                names = get_evolution_names(next_evols_list, names, cont)
                return names

    return names


def request_evolution(evolution_url="", pokemon_root=True):
    """
    Obtiene los datos de los pokemons de la cadena de evolución.
    Parametros:
    - evolution_url: url de la cadena de evolución del pokemon
    https://pokeapi.co/api/v2/evolution-chain/{id}/
    - pokemon_root: chequea si el pokemon es la raiz de su cadena de evolución
        * True si es la raíz
        * False si no es la raíz
    Return:
    - data_evolutions: lista con información de cada uno de los
    pokemons (id, nombre, peso, altura, estadísticas base).
    - evol_parents_idx: lista de banderas para saber de quien
    evoluciona cada pokemon.
    - pokemon_info_root:
        * si pokemoon_root es True: pokemon_info_root es un diccionario
        con información del pokemon raíz
        * si pokemoon_root es False: pokemon_info_root es un diccionario
        vacío.
    """
    response_evolutions = requests.get(evolution_url)
    if response_evolutions.status_code == 200:
        payload_evolutions = response_evolutions.json()
        chain = payload_evolutions.get("chain", {})
        if not pokemon_root:  # si no es pokemon raíz
            root_specie = chain.get("species")
            root_url = root_specie.get("url")
            root_pok_id = re.findall("[0-9]+", root_url)[1]
            url_pok = "https://pokeapi.co/api/v2/pokemon/"
            pokemon_info_root = request_pokemon(url_pok, id_pok=root_pok_id)
        else:
            pokemon_info_root = {}
        list_evolution_names = []
        copy_chain = copy.deepcopy(chain)
        evols_to = chain.get("evolves_to")
        names = []
        i = 0
        lista_names = get_evolution_names(evols_to, names, i)
        evol_names = []
        evol_parents_idx = []
        print("lista names evolutions", lista_names)
        for name_idx in lista_names:
            lista = name_idx.split("_")
            evol_names.append(lista[0])
            evol_parents_idx.append(lista[1])
        data_evolutions = get_evolution_data(evol_names)
        return data_evolutions, evol_parents_idx, pokemon_info_root


def request_species(species_url=""):
    """
    Obtiene la url de la cadena de evolución del pokemon,
    evalua si este pokemon es el pokemon raíz de su cadena de evolución.
    Parametros:
    - species_url: url de las especies
    https://pokeapi.co/api/v2/pokemon-species/{id}/
    Return:
    - evolution_url: url de la cadena de evolución del pokemon
    https://pokeapi.co/api/v2/evolution-chain/{id}/
    - pokemon_root: chequea si el pokemon es la raiz de su cadena de evolución
        * True si es la raíz
        * False si no es la raíz
    """
    response_specie = requests.get(species_url)
    pokemon_root = True
    if response_specie.status_code == 200:
        payload_specie = response_specie.json()
        # chequear si es el pokemon raíz
        evolves_from = payload_specie.get("evolves_from_species", {})
        if evolves_from:
            pokemon_root = False

        evolution_chain = payload_specie.get("evolution_chain")
        evolution_url = evolution_chain.get("url", "")  # incluye el id

        return evolution_url, pokemon_root


def request_pokemon(url_pok="", id_pok=None, name=None):
    """
    Obtiene información del pokemon con id=id_pok o nombre=name.
    parametros:
    - id_pok: id del pokemon para consumir la PokeApi
    - name: nombre del pokemon
    Return:
    pokemon_info: diccionario con la información del pokemon (id, nombre,
    peso, altura, estadísticas base).
    """
    url_pokemon = url_pok
    if id_pok is not None and url_pok == "https://pokeapi.co/api/v2/pokemon/":
        url_pokemon = "{}/{}".format(url_pok, id_pok)
    elif name is not None and url_pok == "https://pokeapi.co/api/v2/pokemon/":
        url_pokemon = "{}/{}".format(url_pokemon, name)

    pokemon_info = {}
    time.sleep(0.2)
    response = requests.get(url_pokemon)
    if response.status_code == 200:
        payload = response.json()

        pokemon_info["id"] = payload.get("id", 0)
        pokemon_info["name"] = payload.get("name", 0)
        pokemon_info["height"] = payload.get('height', 0)
        pokemon_info["weigth"] = payload.get('weight', 0)
        stats = payload.get('stats', [])
        new_stats = []
        temp = {}
        for stat in stats:
            dict2 = stat.get("stat", {})
            temp["name"] = dict2.get("name", "")
            temp["base_stat"] = stat.get("base_stat", 0)
            new_stats.append(temp.copy())
            temp = {}
        pokemon_info["stats"] = new_stats
        species = payload.get("species")
        species_url = species.get("url", "")

        pokemon_info["species_url"] = species_url

    return pokemon_info


def search_byid(id_pok=None):
    """
    Busca por id un pokemon y su respectiva cadena de evolución.
    parametros:
    - id_pok: id del pokemon.
    Return:
    - si todo funciona correctamente:
        * pokemons_data: datos del pokemon con id=id_pok y los pokemons
        de su cadena de evolución.
        * evolution_flags: lista de banderas para saber de quien
        evoluciona cada pokemon.
    - caso contrario retorna None, None
    """
    url_pokemon = 'https://pokeapi.co/api/v2/pokemon/'
    pokemon_info = request_pokemon(url_pokemon, id_pok=id_pok)

    species_url = pokemon_info.get("species_url", "")
    if species_url:
        evolution_url, pokemon_root = request_species(species_url)
        if evolution_url:
            pokemons_data, evolution_flags, pokemon_info_root = request_evolution(evolution_url, pokemon_root)
            if not pokemon_root:
                pokemon_info = pokemon_info_root
            pokemons_data.insert(0, pokemon_info)
            evolution_flags.insert(0, -1)
            return pokemons_data, evolution_flags

    return None, None
