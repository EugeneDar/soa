import subprocess
import time
import requests
import pytest


REST_API = 'http://localhost:8000'

PATH_TO_DOCKER_COMPOSE = '../services'


@pytest.fixture(scope="module", autouse=True)
def setup_compose():
    print("Starting Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "up", "-d", "--build"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)
    time.sleep(20)  # because of long connection to database

    yield

    print("Stopping and cleaning up Docker Compose...")
    subprocess.run(["sudo", "docker-compose", "down", "--volumes"], check=True, cwd=PATH_TO_DOCKER_COMPOSE)


def test_user_modification():
    user_data = {
        "username": "test_user",
        "password": "test_password",
        "phone": "8-800-53-53-535"
    }
    response = requests.post(f"{REST_API}/signup", json=user_data)
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['phone'] == user_data['phone']

    user_data = {
        "username": "test_user",
        "password": "wrong_password"
    }
    response = requests.post(f"{REST_API}/login", json=user_data)
    assert response.status_code == 401
    assert response.json()["message"] == 'Invalid credentials'

    user_data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = requests.post(f"{REST_API}/login", json=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json()
    access_token = response.json()['access_token']

    updated_user_data = {
        "email": "testuser@example.com"
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.put(f"{REST_API}/users/test_user", json=updated_user_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_user_data["email"]
