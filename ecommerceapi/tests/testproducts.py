from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, OrderProduct, Product, ProductType, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

class TestProducts(TestCase):

    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user =  User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, address="111 test road", phone_number="5555555555")
        

    def testListProducts(self):
        ''' Set up all foreign databases that are needed'''
        toys = ProductType.objects.create(name="Toys")
        furby = Product.objects.create(
            title="Furby",
            customer_id=1,
            price=3.00,
            description="Demon baby from hell",
            quantity=4, 
            location="Nashville",
            image_path="https://upload.wikimedia.org/wikipedia/en/7/70/Furby_picture.jpg",
            created_at="2020-06-03 00:00:00Z",
            product_type_id = 1)
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")
        order = Order.objects.create(
            customer_id = 1, 
            payment_type_id=1, 
            created_at="2020-05-29 16:29:18.874982Z")
        order_product = OrderProduct.objects.create(order_id = 1, product_id = 1)
        order_product_two = OrderProduct.objects.create(order_id = 1, product_id = 1)
        
        response = self.client.get(
            reverse('products-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        #check that the status code is 200 and the response is good!
        self.assertEqual(response.status_code, 200)

        #check that there is only one object in the list
        self.assertEqual(len(response.data), 1)
        
        #check that the amount sold is 2 NOT 0 (by default it is 0 but the list method converts it the number based on order-products)
        self.assertEqual(response.data[0]["amount_sold"], 2)



