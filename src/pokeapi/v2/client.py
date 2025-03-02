import aiohttp
from async_lru import alru_cache
from pydantic import BaseModel

from .models import Pokemon, PokemonSpecies
from .resource import NamedApiResourceList

class PokeApiClient:

    def __init__(self, endpoint: str = "https://pokeapi.co"):
        self.endpoint = endpoint
        self._session = aiohttp.ClientSession()


    async def __aenter__(self):
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._session.__aexit__(exc_type, exc_value, traceback)


    async def pokemon(self, id_or_name: int | str) -> Pokemon:
        return await self._get_resource('pokemon', id_or_name, Pokemon)

    async def pokemon_list(self) -> NamedApiResourceList[Pokemon]:
        return await self._get_resource_list('pokemon', Pokemon)

    async def pokemon_species(self, id_or_name: int | str) -> PokemonSpecies:
        return await self._get_resource('pokemon-species', id_or_name, PokemonSpecies)

    async def pokemon_species_list(self) -> NamedApiResourceList[PokemonSpecies]:
        return await self._get_resource_list('pokemon-species', PokemonSpecies)


    async def _get_resource[M: BaseModel](self, resource: str, id_or_name: str | int, clas: type[M]) -> M:
        return await self._get_model(f'{self.endpoint}/api/v2/{resource}/{id_or_name}', clas)

    async def _get_resource_list[M: BaseModel](self, resource: str, clas: type[M]) -> NamedApiResourceList[M]:
        return await self._get_model(f'{self.endpoint}/api/v2/{resource}?limit=10000', NamedApiResourceList[clas])

    @alru_cache(maxsize=None)
    async def _get_model[M: BaseModel](self, url: str, clas: type[M]) -> M:
        """Downloads JSON from a given URL, parses it, and memoizes it."""
        async with self._session.get(url) as response:
            json_response = await response.json()
            return clas.model_validate(json_response)
