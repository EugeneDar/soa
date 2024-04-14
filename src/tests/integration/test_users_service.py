import os
import time
import unittest
import requests
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.compose import DockerCompose

compose_file_path = os.path.abspath('../services')


class UserServiceTests(unittest.TestCase):
    container = None
    users_service_url = None

    @classmethod
    def setUpClass(cls):
        cls.users_service_url = "http://localhost:8000"

        cls.compose = DockerCompose(compose_file_path)
        cls.compose.start()

        # Waiting for services starting
        max_retries = 5
        retry_delay = 3

        for i in range(max_retries):
            try:
                healthcheck_url = f"{cls.users_service_url}/healthcheck"
                response = requests.get(healthcheck_url)
                if response.status_code == 200 and response.json()['status'] == 'OK':
                    break
            except requests.exceptions.RequestException:
                pass

            if i == max_retries - 1:
                raise Exception("Service did not become available within the specified timeout.")

            time.sleep(retry_delay)

    @classmethod
    def tearDownClass(cls):
        cls.container.stop()

    def test_create_user(self):
        user_data = {
            "username": "testuser",
            "password": "testpassword",
            "phone": "8-800-53-53-535"
        }
        response = requests.post(f"{self.users_service_url}/signup", json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["phone"], user_data["phone"])

    def test_create_user_existing_username(self):
        user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(f"{self.users_service_url}/signup", json=user_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "User with such username already exists.")

    def test_login(self):
        user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(f"{self.users_service_url}/login", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("user_id", response.json())

    def test_login_invalid_credentials(self):
        user_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = requests.post(f"{self.users_service_url}/login", json=user_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["message"], "Invalid credentials")

    def test_update_user(self):
        user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(f"{self.users_service_url}/login", json=user_data)
        access_token = response.json()["access_token"]

        updated_user_data = {
            "email": "testuser@example.com"
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.put(f"{self.users_service_url}/users/testuser", json=updated_user_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], updated_user_data["email"])

    def test_update_user_unauthorized(self):
        updated_user_data = {
            "email": "testuser@example.com"
        }
        response = requests.put(f"{self.users_service_url}/users/testuser", json=updated_user_data)
        self.assertEqual(response.status_code, 401)
        raise ValueError(str(response.json()))
        self.assertEqual(response.json()["message"], "Unauthorized request")
