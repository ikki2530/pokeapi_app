from .models import Pokemon, PokemonEvolucion, Evolucion


def guardar_pokemons(pokemons_data):
    """
    Crea y guardar los pokemons en basede datos.
    Parametros:
    - pokemons_data: lista con id, nombre, altura, peso,
    stadísticas base de cada pokemon.
    Return: None
    """
    # crear pokemons
    for pokemon_dict in pokemons_data:
        id_pokemon = pokemon_dict.get("id", None)
        name = pokemon_dict.get("name", "")
        height = pokemon_dict.get("height", 0)
        weigth = pokemon_dict.get("weigth", 0)
        list_stats = pokemon_dict.get("stats", [])
        dict_stats = {}
        for stat in list_stats:
            key = stat.get("name", "")
            value = stat.get("base_stat", 0)
            dict_stats[key] = value
        sp_att = "special-attack"
        sp_def = "special-defense"
        Pokemon.objects.create(id_pokemon=id_pokemon, nombre=name,
                               hp=dict_stats.get("hp"),
                               ataque=dict_stats.get("attack"),
                               defensa=dict_stats.get("defense"),
                               ataque_especial=dict_stats.get(sp_att),
                               defensa_especial=dict_stats.get(sp_def),
                               velocidad=dict_stats.get("speed"),
                               peso=weigth, altura=height)

        # crear otra tabla
        PokemonEvolucion.objects.create(id_pokemon=id_pokemon, nombre=name)


def evolution_relations(pokemons_data=[], evolution_flags=[]):
    """
    Crear relaciones de evolución entre los pokemon obtenidos de la PokeAPi
    Parametros:
    - pokemons_data: lista con id, nombre, altura, peso,
    stadísticas base de cada pokemon.
    - evolution_flags: banderas para crear las relaciones de
    evolución entre los pokemons
    Return: None
    """
    guardar_pokemons(pokemons_data)

    # relaciones de preevolución y postevolución
    pok_idx = 0
    lg = len(evolution_flags)
    tipo_evol = ["PreEvolucion", "PostEvolucion"]
    save_idx = -1
    for i in range(lg):
        id_pokemon = pokemons_data[i].get("id")

        if evolution_flags[i] == -1:
            # root
            pokemon = Pokemon.objects.get(id_pokemon=id_pokemon)
            if lg > 1:
                id_pokemon_evol = pokemons_data[i+1].get("id")
                pokemon_evol = PokemonEvolucion.objects.get(
                               id_pokemon=id_pokemon_evol)
                Evolucion.objects.create(pokemon=pokemon,
                                         pokemon_evolucion=pokemon_evol,
                                         tipo_evolucion=tipo_evol[1])
        else:
            # preevolucion
            idx_parent = int(evolution_flags[i])

            pokemon = Pokemon.objects.get(id_pokemon=id_pokemon)
            id_pokemon_preevol = pokemons_data[idx_parent].get("id")
            pokemon_preevol = PokemonEvolucion.objects.get(
                              id_pokemon=id_pokemon_preevol)
            Evolucion.objects.create(pokemon=pokemon,
                                     pokemon_evolucion=pokemon_preevol,
                                     tipo_evolucion=tipo_evol[0])
            if idx_parent == save_idx:
                id_pokemon_parent = pokemons_data[idx_parent].get("id")
                pokemon_parent = Pokemon.objects.get(
                                 id_pokemon=id_pokemon_parent)
                pokemon_postevol_id = pokemons_data[i].get("id")
                pokemont_son = PokemonEvolucion.objects.get(
                               id_pokemon=pokemon_postevol_id)
                Evolucion.objects.create(pokemon=pokemon_parent,
                                         pokemon_evolucion=pokemont_son,
                                         tipo_evolucion=tipo_evol[1])
                continue
            save_idx = idx_parent
            # postevolucion
            if i < lg - 1:
                id_pokemon_postevol = pokemons_data[i+1].get("id")
                pokemon_postevol = PokemonEvolucion.objects.get(
                                   id_pokemon=id_pokemon_postevol)
                Evolucion.objects.create(pokemon=pokemon,
                                         pokemon_evolucion=pokemon_postevol,
                                         tipo_evolucion=tipo_evol[1])
