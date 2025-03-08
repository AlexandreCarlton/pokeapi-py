
from pokeapi.v2.client import PokeApiClient
from pokeapi.v2.models import Pokemon
from pokeapi.v2.resource import NamedApiResource

async def test_first_element(client: PokeApiClient):
    pokemon_list = await client.pokemon_list(limit=10000)
    assert pokemon_list.results[0] == NamedApiResource[Pokemon](
            name='bulbasaur', 
            url='http://localhost:8080/api/v2/pokemon/1/') 
