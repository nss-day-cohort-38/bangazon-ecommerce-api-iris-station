from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import json


class TestUser(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        self.user = User.objects.create_user(
            username="JohnnyBoy",
            password="Test123",
            email="JohnnyBoy@me.com",
            first_name="Johnny",
            last_name="Boy"
        )

    def testGet(self):
        # Get request for user created in setup
        response = self.client.get("/users/1")

        # Checks to make sure get request went through
        self.assertEqual(response.status_code, 200)
        data = response.data

        # Checks to make sure all data is correct
        self.assertEqual(data["first_name"], "Johnny")
        self.assertEqual(data["last_name"], "Boy")
        self.assertEqual(data["username"], "JohnnyBoy")
        self.assertEqual(data["email"], "JohnnyBoy@me.com")

        # Get request for user that does not exist
        response = self.client.get("/users/2")

        # Checks that error is correct if user does not exist
        # Content is in bit so .decode conerts bytes to string
        self.assertEqual(response.content.decode("utf-8"),
                         "User matching query does not exist.")

    def testEdit(self):

        put_response = self.client.put(
            "/users/1", json.dumps({"username": "JoannaGirl", "first_name": "Joanna", "last_name": "Girl", "email": "JoannaGirl@me.com"}), content_type="application/json")

        # Put request went through correctly
        self.assertEqual(put_response.status_code, 204)

        # Gets updated version on user 1
        get_response = self.client.get("/users/1")

        # Checks updated values
        data = get_response.data
        self.assertEqual(data["first_name"], "Joanna")
        self.assertEqual(data["last_name"], "Girl")
        self.assertEqual(data["username"], "JoannaGirl")
        self.assertEqual(data["email"], "JoannaGirl@me.com")


if __name__ == '__main__':
    unittest.main()
