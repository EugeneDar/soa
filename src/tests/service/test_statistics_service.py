import subprocess
import time
import requests
import unittest


class TestMyService(unittest.TestCase):
    users_service_url = 'http://localhost:8000'
    path_to_docker = './src/services'

    @classmethod
    def setUpClass(cls):
        # subprocess.run(['docker-compose', 'build', cls.path_to_docker], check=True)
        # subprocess.run(['docker-compose', 'up', '-d', cls.path_to_docker], check=True)

        time.sleep(10)  # время ожидания, чтобы контейнер заработал

    @classmethod
    def tearDownClass(cls):
        # Останавливает docker-compose
        # subprocess.run(['docker-compose', 'down'], check=True)
        pass

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


if __name__ == '__main__':
    unittest.main()
