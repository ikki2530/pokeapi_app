from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Perfil(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    fecha_creado = models.DateTimeField(auto_now_add=True, null=True)


class Pokemon(models.Model):
    id_pokemon = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)
    # base stats
    hp = models.IntegerField()
    ataque = models.IntegerField()
    defensa = models.IntegerField()
    ataque_especial = models.IntegerField()
    defensa_especial = models.IntegerField()
    velocidad = models.IntegerField()
    peso = models.IntegerField()
    altura = models.IntegerField()

class PokemonEvolucion(models.Model):
    id_pokemon = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

class Evolucion(models.Model):
    """
    Tabla de relación many to many de Pokemon y PokemonEvolucion
    """
    TIPOS = (
        ('PreEvolucion', 'PreEvolucion'),
        ('PostEvolucion', 'PostEvolucion')
    )
    pokemon = models.ForeignKey(Pokemon, null=True, on_delete= models.SET_NULL)
    pokemon_evolucion = models.ForeignKey(PokemonEvolucion, null=True, on_delete= models.SET_NULL)
    tipo_evolucion = models.CharField(max_length=100, null=True, choices=TIPOS)
