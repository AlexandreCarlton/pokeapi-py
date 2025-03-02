
from pydantic import BaseModel

from .load_json import load_json
from .models import Pokemon, PokemonSpecies
from .resource import NamedApiResourceList

class PokeApiClient:

    def __init__(self, endpoint: str = "https://pokeapi.co"):
        self.endpoint = endpoint

    def pokemon(self, id_or_name: int | str) -> Pokemon:
        return self._get_resource('pokemon', id_or_name, Pokemon)

    def pokemon_list(self) -> NamedApiResourceList[Pokemon]:
        return self._get_resource_list('pokemon', Pokemon)

    def pokemon_species(self, id_or_name: int | str) -> PokemonSpecies:
        return self._get_resource('pokemon-species', id_or_name, PokemonSpecies)

    def pokemon_species_list(self) -> NamedApiResourceList[PokemonSpecies]:
        return self._get_resource_list('pokemon-species', PokemonSpecies)


    def _get_resource[M: BaseModel](self, resource: str, id_or_name: str | int, clas: type[M]) -> M:
        return clas.model_validate(load_json(f'{self.endpoint}/api/v2/{resource}/{id_or_name}'))

    def _get_resource_list[M: BaseModel](self, resource: str, clas: type[M]) -> NamedApiResourceList[M]:
        return NamedApiResourceList[clas].model_validate(load_json(f'{self.endpoint}/api/v2/{resource}?limit=10000'))
