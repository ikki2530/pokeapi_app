# Generated by Django 3.1.6 on 2021-05-11 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='apellido',
        ),
        migrations.AddField(
            model_name='perfil',
            name='fecha_creado',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
