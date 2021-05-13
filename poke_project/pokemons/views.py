from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

# customize
from .models import Pokemon, PokemonEvolucion, Evolucion
from .decorators import unauthenticated_user
from .forms import CreateUserForm
from .pokemons2 import search_byid
from .evolutions import evolution_relations


def RepresentsInt(s):
    """
    chequear si un string es entero o no
    parametros:
    - s: string
    Return:
    - True si es entero
    - False si no es entero
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


@login_required(login_url='login')
def index(request):
    """
    Página principal, para consumir PokeApi por Id
    """
    if request.method == "POST":
        id_pokemon = request.POST.get("pokemon_id")
        id_isnumb = RepresentsInt(id_pokemon)
        if id_isnumb:
            id_pokemon = int(id_pokemon)
            if id_pokemon > 0:

                # chequear si el id ya está en la base de datos
                if Pokemon.objects.filter(id_pokemon=id_pokemon).exists():
                    msg = f"""Pokemon con Id {str(id_pokemon)} ya
                    está en base de datos"""
                    messages.info(request, msg)
                else:
                    # código para descargar datos
                    pokemons_data, evolution_flags = search_byid(id_pokemon)

                    if pokemons_data and evolution_flags:
                        evolution_relations(pokemons_data, evolution_flags)
                        messages.success(request, "Descarga exitosa!!")
                    else:
                        mg = "Id no encontrado en la PokeApi"
                        messages.info(request, mg)
            else:
                messages.info(request, 'Id debe ser mayor que 0')
        else:
            messages.info(request, id_pokemon + ' no es un número entero')

    context = {}
    return render(request, './index.html', context)


@unauthenticated_user
def registerPage(request):
    """
    Registrar nuevos usuarios
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # signal se llama después de esto
            username = form.cleaned_data.get('username')
            messages.success(request, 'Cuenta creada para ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, './register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Usuario o contraseña incorrecta")
    context = {}
    return render(request, './login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@api_view(['GET'])
def pokemonList(request):
    """
    Serializar los pokemons
    """
    name = request.query_params.get("name", "")
    response = {}
    if name:
        if Pokemon.objects.filter(nombre=name).exists():
            pokemon = Pokemon.objects.get(nombre=name)
            id_pokemon = pokemon.id_pokemon
            response["id_pokemon"] = id_pokemon
            response["nombre"] = pokemon.nombre
            response["peso"] = pokemon.peso
            response["altura"] = pokemon.altura
            estadisticas = {
                "hp": pokemon.hp,
                "ataque": pokemon.ataque,
                "defensa": pokemon.defensa,
                "ataque_especial": pokemon.ataque_especial,
                "defensa_especial": pokemon.defensa_especial,
                "velocidad": pokemon.velocidad
            }
            response["estadisticas_base"] = estadisticas

            evolutions = Evolucion.objects.filter(pokemon=pokemon)
            evolution_list = []
            temp = {}
            i = 0
            for evol in evolutions.iterator():
                pokemon_evol = evol.pokemon_evolucion
                poke_evol_id = pokemon_evol.id_pokemon
                poke_evol_name = pokemon_evol.nombre
                pokemon_evol_tipo = evol.tipo_evolucion
                temp["id_evolucion"] = poke_evol_id
                temp["nombre_evolucion"] = poke_evol_name
                temp["tipo_evolucion"] = pokemon_evol_tipo
                evolution_list.append(temp)
                temp = {}
            response["cadena_evolucion"] = evolution_list
        else:
            mg = "No existe el nombre " + name + " en la base de datos"
            response["mensaje"] = mg
    else:
        response["mensaje"] = "envía el parámetro 'name'"
    return JsonResponse(response)
