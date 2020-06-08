from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, ProductType, Product, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import unittest
import django.contrib.sites.requests

"""
- No Retrieve
- No Update
- No Destroy
"""

class TestProductTypes(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        pass

    def test_list_product_type(self):
        # watches = ProductType.objects.create(name="Watches")
        # response = self.client.get(
        #     reverse('producttypes-list'), HTTP_AUTHORIZATION='Token' + str(self.token))
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(watches.name.encode(), response.content)
        pass


    def testPost(self):
        pass


    def testList(self):
        pass


    def testNumberQuery(self):
        pass



if __name__ == '__main__':
    unittest.main()
