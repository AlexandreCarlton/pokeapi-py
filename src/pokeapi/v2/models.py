"""
Species all models used for loading data.

Naming should derive from https://pokeapi.co/docs/v2
"""

from typing import Optional

from pydantic import BaseModel

from pokeapi.v2.resource import ApiResource, NamedApiResource

class NamedBaseModel(BaseModel):
    """Provides attributes common to all named models"""
    id: int
    name: str


class Characteristic(BaseModel):
    id: int

class Pokemon(NamedBaseModel):
    height: int
    species: NamedApiResource['PokemonSpecies']
    sprites: 'PokemonSprites'
    stats: list['PokemonStat']
    weight: int
    # Regrettably, this is not an ApiResource - see https://github.com/PokeAPI/pokeapi/issues/332
    location_area_encounters: str

class PokemonColor(NamedBaseModel):
    pokemon_species: list[NamedApiResource['PokemonSpecies']]

class PokemonSpecies(NamedBaseModel):
    base_happiness: Optional[int]
    capture_rate: int
    color: NamedApiResource['PokemonColor']

class PokemonSprites(BaseModel):
    front_default: Optional[str]

class PokemonStat(BaseModel):
    base_stat: int
    effort: int
    stat: NamedApiResource['Stat']

class Stat(NamedBaseModel):
    game_index: int
    characteristics: list[ApiResource['Characteristic']]
    is_battle_only: bool
