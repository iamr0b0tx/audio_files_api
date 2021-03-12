import io
import pytest

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_base_endpoint_get(client):
    """ test base endpoint """

    response = client.get('/')
    assert response.status_code == 404


def test_ping_get(client):
    """ test ping endpoint """

    response = client.get('/ping')
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["status"] == 1
    assert response_data["data"] == "pong"

