from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Product
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

"""
- No Retrieve
- No Update
- No Destroy
"""

class TestProductTypes(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        pass

    def testPost(self):
        pass
    
    def testList(self):
        pass

    def testNumberQuery(self):
        pass

    

if __name__ == '__main__':
    unittest.main()
