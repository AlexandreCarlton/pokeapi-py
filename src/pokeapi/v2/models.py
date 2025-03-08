"""
Species all models used for loading data.

Naming should derive from https://pokeapi.co/docs/v2
"""

from pokeapi.v2.base import PokeApiBaseType
from pokeapi.v2.resource import ApiResource, NamedApiResource


class NamedPokeApiType(PokeApiBaseType):
    """Provides attributes common to all named models"""
    id: int
    name: str


class Characteristic(PokeApiBaseType):
    id: int

class Pokemon(NamedPokeApiType):
    height: int
    species: NamedApiResource['PokemonSpecies']
    sprites: 'PokemonSprites'
    stats: list['PokemonStat']
    weight: int
    # Regrettably, this is not an ApiResource - see https://github.com/PokeAPI/pokeapi/issues/332
    location_area_encounters: str

class PokemonColor(NamedPokeApiType):
    pokemon_species: list[NamedApiResource['PokemonSpecies']]

class PokemonSpecies(NamedPokeApiType):
    base_happiness: int | None
    capture_rate: int
    color: NamedApiResource['PokemonColor']

class PokemonSprites(PokeApiBaseType):
    front_default: str | None

class PokemonStat(PokeApiBaseType):
    base_stat: int
    effort: int
    stat: NamedApiResource['Stat']

class Stat(NamedPokeApiType):
    game_index: int
    characteristics: list[ApiResource['Characteristic']]
    is_battle_only: bool
