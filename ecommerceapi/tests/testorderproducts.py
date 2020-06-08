from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Product, Customer, Order, OrderProduct, ProductType, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import json

"""
- Maybe this will work
"""


class TestOrderProducts(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        pass
        self.username = "HotDog"
        self.password = "HotDogs"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user_id=1, address="808 Hot Dog Highway", phone_number="615-HOT-DOGS")

        thisOrder = Order.objects.create(
            created_at="2020-06-03 00:00:00Z",
            customer_id=1,
            payment_type_id=1)
        furby = Product.objects.create(
            title="Furby",
            customer_id=1,
            price=3800.71,
            description="Demon baby from hell",
            quantity=4,
            location="Nashville",
            image_path="https://upload.wikimedia.org/wikipedia/en/7/70/Furby_picture.jpg",
            created_at="2020-06-03 00:00:00Z",
            product_type_id=1)
        toys = ProductType.objects.create(name="Toys")
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company",
            account_number="1234123412341234",
            expiration_date="2024-01-01",
            customer_id=1,
            created_at="2020-05-27 15:08:30.518598Z")

    def testPost(self):
        # Post
        response = self.client.post(
            "/order_products", json.dumps({"order_id": 1, "product_id": 1}), content_type="application/json")

        # Check for correct http response
        self.assertEqual(response.status_code, 200)

        # Get all orderproducts
        response = self.client.get(
            reverse('orderproducts-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that there is only 1 object in the response
        self.assertEqual(len(response.data), 1)

    def testList(self):
        # Create the necessary data
        order_product = OrderProduct.objects.create(order_id=1, product_id=1)

        # Get response
        response = self.client.get(
            reverse('orderproducts-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check for proper http response
        self.assertEqual(response.status_code, 200)

        # Check that there is just 1 object in the response
        self.assertEqual(len(response.data), 1)

    def testDelete(self):
        # Create the necessary data
        order_product = OrderProduct.objects.create(order_id=1, product_id=1)

        # Get response
        response = self.client.get(
            reverse('orderproducts-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that there is just 1 object in the response
        self.assertEqual(len(response.data), 1)

        # Check for proper http response
        self.assertEqual(response.status_code, 200)

        #  Delete the orderproduct with id = 1
        response = self.client.delete('/order_products/1')

        # Check for proper http response
        self.assertEqual(response.status_code, 204)

        # Check that there are 0 objects in the response
        self.assertEqual(len(response.data), 0)


if __name__ == '__main__':
    unittest.main()
