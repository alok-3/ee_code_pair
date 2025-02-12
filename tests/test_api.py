import pytest
from src.api import api

@pytest.fixture
def client():
    with api.test_client() as client:
        yield client

def test_get_gists_valid_user(client):
    response = client.get('/octocat')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_gists_invalid_user(client):
    response = client.get('/nonexistentuser123456789')
    assert response.status_code == 404
    assert response.json.get("error") == "User not found"

def test_pagination(client):
    response = client.get('/octocat?page=2&per_page=5')
    assert response.status_code == 200
    assert isinstance(response.json, list)
