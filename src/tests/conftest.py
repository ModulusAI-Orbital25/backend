import sys
from os import path

sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), "..")))

import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
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


class AuthActions:
    def __init__(self, client):
        self.client = client

    def register(
        self,
        username="test",
        password="testpassword",
    ):
        return self.client.post(
            "/profile/register",
            json={
                "username": username,
                "password": password,
            },
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
