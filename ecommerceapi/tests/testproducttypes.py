from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, ProductType, Product, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import unittest
import django.contrib.sites.requests


class TestProductTypes(TestCase):
    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, address="111 test road", phone_number="5555555555")
        self.new_watch_instance = ProductType.objects.create(id=4, name="Watches")
        self.new_watch = Product.objects.create(
            title="Rolex",
            customer_id=1,
            price=3.00,
            description="Ball Out",
            quantity=4,
            location="Nashville",
            image_path="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQco0Tx9CnodcYY1PdeAzv6hw2EvWKPMv-TD9A3ig3T5o9TIvhz0yALZ3mzuLc2vkFOZ0IndIU&usqp=CAc",
            created_at="2020-06-03 00:00:00Z",
            product_type_id=4)


    def test_list_product_type(self):
        watches = ProductType.objects.create(name="Watches")
        response = self.client.get(
            reverse('producttypes-list'), HTTP_AUTHORIZATION='Token' + str(self.token))
        self.assertEqual(response.status_code, 200)
        self.assertIn(watches.name.encode(), response.content)

    def test_post_producttype(self):
        pass


if __name__ == '__main__':
    unittest.main()
