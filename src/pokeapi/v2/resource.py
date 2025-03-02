import re
from importlib import import_module
from typing import Generic, TypeVar

from pydantic import BaseModel

from .load_json import load_json

GENERIC_CLASS_PATTERN = re.compile('.+\\[(.+)\\]$')
MODELS_MODULE = import_module('pokeapi.v2.models')

Resource = TypeVar('Resource', bound=BaseModel)

class ApiResource(BaseModel, Generic[Resource]):
    """
    See https://pokeapi.co/docs/v2#apiresource
    """
    url: str

    def load(self) -> Resource:
        """Loads the named resource.
        As PokeAPI does not provide a bulk-fetch API, this is not as terrible
        as it looks."""
        model = self._get_type_parameter()
        return model.model_validate(load_json(self.url))

    def _get_type_parameter(self) -> type[Resource]:
        """Load the type parameter's class hackily as Python 3.13 does not
        offer a way to do this cleanly. """
        match = GENERIC_CLASS_PATTERN.match(self.__class__.__name__)
        if not match:
            raise RuntimeError(f"Class name '{self.__class__.__name__}' did not match {GENERIC_CLASS_PATTERN}")
        resource_class_name = match.group(1)
        return getattr(MODELS_MODULE, resource_class_name)


class NamedApiResource(ApiResource, Generic[Resource]):
    """
    See https://pokeapi.co/docs/v2#namedapiresource
    """
    name: str

class ApiResourceList(BaseModel, Generic[Resource]):
    """
    See https://pokeapi.co/docs/v2#apiresourcelist
    """
    results: list[ApiResource[Resource]]


class NamedApiResourceList(BaseModel, Generic[Resource]):
    """
    See https://pokeapi.co/docs/v2#namedapiresourcelist
    """
    results: list[NamedApiResource[Resource]]
