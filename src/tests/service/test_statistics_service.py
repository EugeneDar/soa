import subprocess
import time
import requests
import unittest


class TestMyService(unittest.TestCase):
    users_service_url = 'http://localhost:8000'
    path_to_docker = './src/services'

    @classmethod
    def setUpClass(cls):
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
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
        # self.assertEqual(response.json()["phone"], user_data["phone"])
        self.assertEqual(response.json()["phone"], "he-he")


if __name__ == '__main__':
    unittest.main()
