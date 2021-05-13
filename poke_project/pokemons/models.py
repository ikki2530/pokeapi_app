from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"id: {str(self.id_pokemon)}, nombre: {self.nombre}"


class PokemonEvolucion(models.Model):
    id_pokemon = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"id: {str(self.id_pokemon)}, nombre: {self.nombre}"

class Evolucion(models.Model):
    """
    Tabla de relación many to many entre Pokemon y PokemonEvolucion
    """
    TIPOS = (
        ('PreEvolucion', 'PreEvolucion'),
        ('PostEvolucion', 'PostEvolucion')
    )
    pokemon = models.ForeignKey(Pokemon, null=True, on_delete= models.SET_NULL)
    pokemon_evolucion = models.ForeignKey(PokemonEvolucion, null=True, on_delete= models.SET_NULL)
    tipo_evolucion = models.CharField(max_length=100, null=True, choices=TIPOS)

    def __str__(self):
        return f"pokemon: ({self.pokemon}) -- pokemon {self.tipo_evolucion}: ({self.pokemon_evolucion})"
