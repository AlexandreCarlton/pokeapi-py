"""
Common fixture to be used across all tests.

See https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
"""

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from pokeapi.v2.client import PokeApiClient

PORT = 8080
ENDPOINT = f'http://localhost:{PORT}'
IMAGE = 'docker.io/alexandrecarlton/pokeapi-dump:sha-aff23d7'

@pytest.fixture(scope="session", autouse=True)
def pokeapi_container(request):
    """Starts the pokeapi dump container and returns a client for it."""
    pokeapi = (DockerContainer(IMAGE)
               .with_env('ENDPOINT', ENDPOINT)
               .with_bind_ports(80, PORT))
    pokeapi.start()
    wait_for_logs(pokeapi, 'Configuration complete; ready for start up')
    def remove_container():
        pokeapi.stop()
    request.addfinalizer(remove_container)

@pytest.fixture(scope="session")
def client(request):
    return PokeApiClient(ENDPOINT)
