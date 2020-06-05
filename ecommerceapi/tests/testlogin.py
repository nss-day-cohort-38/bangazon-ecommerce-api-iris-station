from django.test import TestCase
from django.urls import reverse
import ecommerceapi.models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

class TestLogin(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        pass

    def testGetToken(self):
        pass

    def testLoginError(self):
        pass


if __name__ == '__main__':
    unittest.main()
