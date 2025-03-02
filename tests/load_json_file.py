
import json
from typing import Any
from pathlib import Path

def load_json_file(path: str) -> dict[str, Any]:
    filepath = Path('tests') / 'data' / f'{path}.json'
    with filepath.open('r') as file:
        loaded_json = json.load(file)
    return loaded_json
