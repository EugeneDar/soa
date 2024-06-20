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


def test_posts_creation():
    user_data = {
        "username": "test_user",
        "password": "test_password",
    }
    _ = requests.post(f"{REST_API}/signup", json=user_data)

    user_data = {
        "username": "test_user",
        "password": "test_password"
    }
    response = requests.post(f"{REST_API}/login", json=user_data)
    access_token = response.json()['access_token']

    post_data = {
        "title": "War and peace",
        "content": "A lot of words..."
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    _ = requests.post(f"{REST_API}/posts", json=post_data, headers=headers)
    response = requests.post(f"{REST_API}/posts", json=post_data, headers=headers)
    assert response.status_code == 201
    assert response.json()['title'] == 'War and peace'

    post_id = response.json()['id']

    post_data = {
        "title": "Martin Eden",
        "content": "Sad story"
    }
    response = requests.put(f"{REST_API}/posts/{post_id}", json=post_data, headers=headers)
    assert response.json()['title'] == 'Martin Eden'

    response = requests.get(f"{REST_API}/posts/{post_id}", json=post_data, headers=headers)
    assert response.json()['title'] == 'Martin Eden'

    user_data = {
        "user_id": 1
    }
    response = requests.get(f"{REST_API}/posts", json=user_data, headers=headers)
    assert response.json()['total_count'] == 2

    _ = requests.delete(f"{REST_API}/posts/{post_id}", json=post_data, headers=headers)

    response = requests.get(f"{REST_API}/posts", json=user_data, headers=headers)
    assert response.json()['total_count'] == 1
