from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, ProductType, Product, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import unittest



class TestProductTypes(TestCase):
    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

    def test_list_product(self):
        new_product = Product.objects.create(
            title="Rolex",
            customer_id=1,
            price=3.00,
            description="Ball out",
            quantity=4, 
            location="Nashville",
            image_path="https://upload.wikimedia.org/wikipedia/en/7/70/Furby_picture.jpg",
            created_at="2020-06-03 00:00:00Z",
            product_type_id=1
        )
        watches = ProductType.objects.create(name="Watches")
        payment_type = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")
        order = Order.objects.create(
            customer_id = 1, 
            payment_type_id=1, 
            created_at="2020-05-29 16:29:18.874982Z")

        response = self.client.get(reverse('products-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        # self.assertEqual(response.data[0]["amount_sold"], 2)



         #Use the client to send the request and store the response
        # response = self.client.post(reverse('products-form'), new_product)
        # self.assertEqual(response.status_code, 200)

    def test_list_product_type(self):
        watches = ProductType.objects.create(name="Watches")
        response = self.client.get(reverse('producttypes-list'), HTTP_AUTHORIZATION='Token' + str(self.token))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(response.context['producttypes-list']), 1)
        self.assertIn(watches.name.encode(), response.content)

if __name__ == '__main__':
    unittest.main()
