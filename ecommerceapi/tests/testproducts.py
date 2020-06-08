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
        ''' Set up all foreign databases that are needed'''
        toys = ProductType.objects.create(name="Toys")
        furby = Product.objects.create(
            title="Furby",
            customer_id=1,
            price=3.11,
            description="Demon baby from hell",
            quantity=4, 
            location="Nashville",
            image_path="hotdogs.jpg",
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

    def testListProducts(self):
        response = self.client.get(
            reverse('products-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        #check that the status code is 200 and the response is good!
        self.assertEqual(response.status_code, 200)

        #check that there is only one object in the list
        self.assertEqual(len(response.data), 1)
        
        #check that the amount sold is 2 NOT 0 (by default it is 0 but the list method converts it the number based on order-products)
        self.assertEqual(response.data[0]["amount_sold"], 2)
    
    def testPost(self):
        new_product = {
            "title":"Furbot",
            "customer_id": 1,
            "price": 4.11,
            "description": "Knock-off furby",
            "quantity": 4, 
            "location": "Nashville",
            "image_path": "franks.jpg",
            "created_at": "2020-05-27 15:08:30.518598Z",
            "product_type_id": 1
        }
        
        response = self.client.post(
            reverse('products-list'), 
            new_product,
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Product.objects.count(), 2)

        self.assertEqual(Product.objects.get(pk=2).title, new_product["title"])


    def testGet(self):
        response = self.client.get(
            reverse('products-list'), 
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["title"], "Furby")
        # self.assertEqual(response.data[0]["customer_id"], 1)
        
        # Note: decimals need to be serialized as strings 
        # in JSON, "since float representation would lose precision"
        # https://github.com/encode/django-rest-framework/issues/508
        self.assertEqual(response.data[0]["price"], "3.11")
        self.assertEqual(response.data[0]["description"], "Demon baby from hell")
        self.assertEqual(response.data[0]["quantity"], 4)
        self.assertEqual(response.data[0]["location"], "Nashville")
        self.assertEqual(response.data[0]["image_path"], "http://testserver/media/hotdogs.jpg")
        self.assertEqual(response.data[0]["created_at"], "2020-06-03T00:00:00Z")
        self.assertEqual(response.data[0]["product_type_id"], 1)        

    def testDelete(self):
        response = self.client.delete(
            reverse('products-detail', kwargs={'pk': 1}),
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('products-list'), 
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        self.assertEqual(len(response.data), 0)

    def testEdit(self):
        # TODO: 
        # At the moment of this test's creation, the only editing endpoint we have for products is quantity
        
        updated_product = {
            "quantity": 9000,
        }
        
        response = self.client.put(
            reverse('products-detail', kwargs={'pk': 1}),
            updated_product,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(
            reverse('products-detail', kwargs={'pk': 1}), 
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.data["quantity"], updated_product["quantity"])
        
    def testNumberQuery(self):
        # testing the query parameters on list that return
        # the twenty most recent products
        response = self.client.get(
            '/products?number', # Testing the number-specific endpoint
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)        
        self.assertEqual(response.data[0]["amount_sold"], 2)

    def testUserQuery(self):
        # testing the query parameters on list that 
        # returns all the "My Products" for an authenticated user
        response = self.client.get(
            '/products?user', # Testing the user-specific endpoint
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)        
        self.assertEqual(response.data[0]["amount_sold"], 2)
        

