
from typing import Any

import pytest

from pokeapi.v2.client import PokeApiClient
from .load_json_file import load_json_file

PARAMETERS = [
        (1, load_json_file('pokemon-species/1')),
]

@pytest.mark.parametrize('id_or_name,species_json', PARAMETERS)
async def test_base_happiness(client: PokeApiClient, id_or_name: int | str, species_json: dict[str, Any]):
    species = await client.pokemon_species(id_or_name)
    assert species.base_happiness == species_json['base_happiness']
