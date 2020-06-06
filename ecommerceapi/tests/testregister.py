from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import json


class TestRegister(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        self.user_info = {
            "username": "johnnyboy",
            "email": "johnsmith@me.com",
            "password": "test123",
            "first_name": "Johnny",
            "last_name": "Boy",
            "address": "123 Street St",
            "phone_number": "123-456-4567"
        }

    def testGetToken(self):
        json_info = json.dumps(self.user_info)
        response = self.client.post(
            '/register/', json_info, content_type="application/json")

        # Checks the status of post
        self.assertEqual(response.status_code, 200)

        # Checks to see if token is in response
        converted = json.loads(response.content)
        self.assertTrue("token" in converted)

        response = self.client.post(
            '/register/', json_info, content_type="application/json")

        # Checks to see if you cannt add another user with the same username
        converted = response.content.decode("utf-8")
        self.assertTrue(
            "UNIQUE constraint failed: auth_user.username" in converted)


if __name__ == '__main__':
    unittest.main()
