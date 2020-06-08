from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
import json

"""
- Np Retrieve
"""
class TestOrders(TestCase):

    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

    def testDeleteOrder(self):
        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.delete(
            reverse('order-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(len(response.data), 0)

    def testPost(self):
        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get(
            reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # test that there is only one order that has been created 
        self.assertEqual(len(response.data), 1)
        
        self.assertEqual(response.status_code, 200)

        # test that it is indeed the one we created 
        self.assertEqual(response.data[0]["customer"]["id"], 1)
    
    def testList(self):
        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get(
            reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # test that there is only one order that has been created 
        self.assertEqual(len(response.data), 1)

        second_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2019-06-29T14:42:51.221420Z"
        )


        response = self.client.get(
            reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # test for two orders returning under length

        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.status_code, 200)

    def testEdit(self):
        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")
        u_order = {
            "customer_id": 1,
            "payment_type_id": 1,
            "created_at": "2020-05-29T14:42:51.221420Z"
        }
        response = self.client.put(
            reverse('order-detail', kwargs={'pk': 1}),
            u_order,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + str(self.token)
        )

        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.data[0]['payment_type_id'], 1)
        

    # dont use in web app it is set up but it isn't needed.    
    def testPaymentTypeIdQuery(self):
        pass

if __name__ == '__main__':
    unittest.main()
