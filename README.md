# pokeapi-py

A simple (work-in-progress) Python library for querying data through [PokeAPI](https://pokeapi.co/).

It is incomplete, but provides enough of a solid foundation that completing the
remainder of its support should be straightforward.

## Installation

Installation into a virtualenv can be done with the following:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pip install git+https://github.com/AlexandreCarlton/pokeapi-py.git
```

If you are using [`uv`](https://docs.astral.sh/uv/), one can use:

```bash
uv add git+https://github.com/AlexandreCarlton/pokeapi-py.git
```

## Usage

### Simple attributes

The following is a straightforward usage of the client.

```python
from pokeapi.client import PokeApiClient

client = PokeApiClient()
bulbasaur = client.pokemon(1)
print(bulbasaur.name) # 'bulbasaur'
```

### Custom endpoint

By default the client will point to [pokeapi.co](https://pokeapi.co). Should a
different endpoint be desired (e.g. [AlexandreCarlton/pokeapi-dump](https://github.com/AlexandreCarlton/pokeapi-dump`)),
the following can be used:

```python
from pokeapi.client import PokeApiClient

# Connects to a local instance running on 8080.
client = PokeApiClient(endpoint="https://localhost:8080")
```

## FAQ

### Why isn't this uploaded to PyPI?
This is a pet project intended to experiment with the Python ecosystem since
the author last interacted with it (some 7 odd years ago). There are better,
more maintained alternatives (like [aiopokeapi](https://github.com/beastmatser/aiopokeapi),
which shares many of the design goals of this project).
