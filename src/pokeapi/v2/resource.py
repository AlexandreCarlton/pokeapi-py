import re
from importlib import import_module
from typing import TYPE_CHECKING, cast

from pokeapi.v2.base import PokeApiBaseType

if TYPE_CHECKING:
    from pokeapi.v2.client import PokeApiClient

GENERIC_CLASS_PATTERN = re.compile('.+\\[(.+)\\]$')
MODELS_MODULE = import_module('pokeapi.v2.models')

class ApiResource[T: PokeApiBaseType](PokeApiBaseType):
    """
    See https://pokeapi.co/docs/v2#apiresource
    """
    url: str

    async def get(self, client: 'PokeApiClient') -> T:
        """Loads the named resource using the provided client.
        As PokeAPI does not provide a bulk-fetch API, this is not as terrible
        as it looks."""
        model_type = self._get_type_parameter()
        model = await client._get_model(model_type, self.url)
        return cast(T, model)

    def _get_type_parameter(self) -> type[T]:
        """Load the type parameter's class hackily as Python 3.13 does not
        offer a way to do this cleanly. """
        match = GENERIC_CLASS_PATTERN.match(self.__class__.__name__)
        if not match:
            raise RuntimeError(f"Class name '{self.__class__.__name__}' did not match {GENERIC_CLASS_PATTERN}")
        resource_class_name = match.group(1)
        return cast(type[T], getattr(MODELS_MODULE, resource_class_name))


class NamedApiResource[T: PokeApiBaseType](ApiResource[T]):
    """
    See https://pokeapi.co/docs/v2#namedapiresource
    """
    name: str

class ApiResourceList[T: PokeApiBaseType](PokeApiBaseType):
    """
    See https://pokeapi.co/docs/v2#apiresourcelist
    """
    results: list[ApiResource[T]]


class NamedApiResourceList[T: PokeApiBaseType](PokeApiBaseType):
    """
    See https://pokeapi.co/docs/v2#namedapiresourcelist
    """
    results: list[NamedApiResource[T]]
