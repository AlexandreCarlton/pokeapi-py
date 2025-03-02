
from typing import Any

import pytest

from pokeapi.v2.client import PokeApiClient
from pokeapi.v2.resource import NamedApiResource
from pokeapi.v2.models import PokemonSpecies
from .load_json_file import load_json_file

PARAMETERS = [
        (1, load_json_file('pokemon/1')),
        ('bulbasaur', load_json_file('pokemon/1')),
        (10001, load_json_file('pokemon/10001')),
]

@pytest.mark.parametrize('id_or_name,pokemon_json', PARAMETERS)
async def test_height(client: PokeApiClient, id_or_name: int | str, pokemon_json: dict[str, Any]):
    pokemon = await client.pokemon(id_or_name)
    assert pokemon.height == pokemon_json['height']

@pytest.mark.parametrize('id_or_name,pokemon_json', PARAMETERS)
async def test_weight(client: PokeApiClient, id_or_name: int | str, pokemon_json: dict[str, Any]):
    pokemon = await client.pokemon(id_or_name)
    assert pokemon.weight == pokemon_json['weight']

@pytest.mark.parametrize('id_or_name,pokemon_json', PARAMETERS)
async def test_species(client: PokeApiClient, id_or_name: int | str, pokemon_json: dict[str, Any]):
    pokemon = await client.pokemon(id_or_name)
    assert pokemon.species == NamedApiResource[PokemonSpecies](
            name=pokemon_json['species']['name'],
            url=pokemon_json['species']['url'])

@pytest.mark.parametrize('id_or_name,pokemon_json', PARAMETERS)
async def test_species_load(client: PokeApiClient, id_or_name: int | str, pokemon_json: dict[str, Any]):
    pokemon = await client.pokemon(id_or_name)
    species = await pokemon.species.get(client)
    assert isinstance(species, PokemonSpecies)
