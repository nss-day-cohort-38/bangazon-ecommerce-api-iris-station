from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import json


class TestLogin(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        # create a user
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        # create customer
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")
        Token.objects.create(user=self.user)

    def testGetPost(self):
        # Post to login a correct object with uername and password
        response = self.client.post(
            "/login/", json.dumps({"username": "TestUser", "password": "testword1"}), content_type="application/json")
        # Status should be ok
        self.assertEqual(response.status_code, 200)
        # convert json to dictionary
        content = json.loads(response.content)
        # check to see that user id is returned
        self.assertEqual(content["user_id"], 1)
        # check to see that token is returned
        self.assertTrue("token" in content)
        # check to see that valid is true
        self.assertEqual(content["valid"], True)

    def testIncorectUserName(self):
        # Post to login an incorrect password
        response = self.client.post(
            "/login/", json.dumps({"username": "TestUser", "password": "testwor"}), content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        # Response should return {"valid": False}
        self.assertEqual(content["valid"], False)

    def testIncorrectPassword(self):
        # Post to login an incorrect username
        response = self.client.post(
            "/login/", json.dumps({"username": "Test", "password": "testwor"}), content_type="application/json")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["valid"], False)

if __name__ == '__main__':
    unittest.main()
