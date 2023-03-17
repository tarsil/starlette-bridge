import functools

import pytest
from starlette.testclient import TestClient


@pytest.fixture
def no_trio_support(anyio_backend_name):  # pragma: no cover
    if anyio_backend_name == "trio":
        pytest.skip("Trio not supported (yet!)")


@pytest.fixture
def test_client_factory(anyio_backend_name, anyio_backend_options):
    # anyio_backend_name defined by:
    # https://anyio.readthedocs.io/en/stable/testing.html#specifying-the-backends-to-run-on
    return functools.partial(
        TestClient,
        backend=anyio_backend_name,
        backend_options=anyio_backend_options,
    )
