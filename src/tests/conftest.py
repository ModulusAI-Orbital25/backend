import sys
from os import path

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "..")))

import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    # some setup idk
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
