from types import TracebackType
from typing import Tuple, Optional, Sequence, cast

import aiohttp
from async_lru import alru_cache
from pydantic import BaseModel

from pokeapi.v2.models import Pokemon, PokemonSpecies
from pokeapi.v2.resource import NamedApiResourceList

class PokeApiClient:

    def __init__(self, endpoint: str = "https://pokeapi.co"):
        self.endpoint = endpoint
        self._session = aiohttp.ClientSession()


    async def __aenter__(self) -> 'PokeApiClient':
        await self._session.__aenter__()
        return self

    async def __aexit__[E: BaseException](self, exc_type: type[E], exc_value: E, traceback: TracebackType) -> None:
        await self._session.__aexit__(exc_type, exc_value, traceback)


    async def pokemon(self, id_or_name: int | str) -> Pokemon:
        return await self._get_resource('pokemon', id_or_name, Pokemon)

    async def pokemon_list(self, limit: Optional[int]=None, offset: Optional[int]=None) -> NamedApiResourceList[Pokemon]:
        return await self._get_resource_list('pokemon', limit, offset, Pokemon)

    async def pokemon_species(self, id_or_name: int | str) -> PokemonSpecies:
        return await self._get_resource('pokemon-species', id_or_name, PokemonSpecies)

    async def pokemon_species_list(self, limit: Optional[int]=None, offset: Optional[int]=None) -> NamedApiResourceList[PokemonSpecies]:
        return await self._get_resource_list('pokemon-species', limit, offset, PokemonSpecies)


    async def _get_resource[T: BaseModel](self, resource: str, id_or_name: str | int, clas: type[T]) -> T:
        resource = await self._get_model(clas, f'{self.endpoint}/api/v2/{resource}/{id_or_name}')
        return cast(T, resource)

    async def _get_resource_list[T: BaseModel](self, resource: str, limit: Optional[int], offset: Optional[int], clas: type[T]) -> NamedApiResourceList[T]:
        # Mypy wants to be able to resolve this statically but it can't, so we suppress this.
        resource_list_type = NamedApiResourceList[clas] # type: ignore [valid-type]
        resource_list = await self._get_model(resource_list_type, f'{self.endpoint}/api/v2/{resource}', PokeApiClient._to_params(limit, offset))
        return cast(NamedApiResourceList[T], resource_list)


    @staticmethod
    def _to_params(limit: Optional[int]=None, offset: Optional[int]=None) -> Sequence[Tuple[str, int]]:
        return [(key, value)
                for key, value in [('limit', limit), ('offset', offset)]
                if value]


    @alru_cache(maxsize=None)
    async def _get_model[T: BaseModel](self, clas: type[T], url: str, params: Sequence[Tuple[str, int]]=()) -> T:
        """Downloads JSON from a given URL, parses it, and memoizes it."""
        async with self._session.get(url, params=params) as response:
            json_response = await response.json()
            return clas.model_validate(json_response)
