from typing import Tuple, Optional, Sequence

import aiohttp
from async_lru import alru_cache
from pydantic import BaseModel

from pokeapi.v2.models import Pokemon, PokemonSpecies
from pokeapi.v2.resource import NamedApiResourceList

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

    async def pokemon_list(self, limit: Optional[int]=None, offset: Optional[int]=None) -> NamedApiResourceList[Pokemon]:
        return await self._get_resource_list('pokemon', limit, offset, Pokemon)

    async def pokemon_species(self, id_or_name: int | str) -> PokemonSpecies:
        return await self._get_resource('pokemon-species', id_or_name, PokemonSpecies)

    async def pokemon_species_list(self, limit: Optional[int]=None, offset: Optional[int]=None) -> NamedApiResourceList[PokemonSpecies]:
        return await self._get_resource_list('pokemon-species', limit, offset, PokemonSpecies)


    async def _get_resource[M: BaseModel](self, resource: str, id_or_name: str | int, clas: type[M]) -> M:
        return await self._get_model(clas, f'{self.endpoint}/api/v2/{resource}/{id_or_name}')

    async def _get_resource_list[M: BaseModel](self, resource: str, limit: Optional[int], offset: Optional[int], clas: type[M]) -> NamedApiResourceList[M]:
        # Mypy wants to be able to resolve this statically but it can't, so we suppress this.
        resource_list_type = NamedApiResourceList[clas] # type: ignore
        return await self._get_model(resource_list_type, f'{self.endpoint}/api/v2/{resource}', PokeApiClient._to_params(limit, offset)) # type: ignore

    @staticmethod
    def _to_params(limit: Optional[int]=None, offset: Optional[int]=None) -> Sequence[Tuple[str, int]]:
        return [(key, value)
                for key, value in [('limit', limit), ('offset', offset)]
                if value]


    @alru_cache(maxsize=None)
    async def _get_model[M: BaseModel](self, clas: type[M], url: str, params: Sequence[Tuple[str, int]]=()) -> M:
        """Downloads JSON from a given URL, parses it, and memoizes it."""
        async with self._session.get(url, params=params) as response:
            json_response = await response.json()
            return clas.model_validate(json_response)
