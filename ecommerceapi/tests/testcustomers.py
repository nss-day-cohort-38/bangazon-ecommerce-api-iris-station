from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip
"""
- No Create
- No destroy
"""

class TestCustomers(TestCase):
    def createOrders(self):
        Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        
    def createPaymentType(self):
        PaymentType.objects.create(
            merchant_name="Merchant Name",
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        
    def createCustomer(self):
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555"
        )

    def setUp(self):
        self.username_1 = "TestUser"
        self.password_1 = "testword1"
        self.user_1 = User.objects.create_user(
            username=self.username_1, password=self.password_1)
        self.token_1 = Token.objects.create(user=self.user_1)

        self.username_2 = "TestUser2"
        self.password_2 = "testword2"
        self.user_2 = User.objects.create_user(
            username=self.username_2, password=self.password_2)
        self.token_2 = Token.objects.create(user=self.user_2)


    def testOrderCount(self):
        self.createPaymentType()

        self.createCustomer()

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], 0)

        self.createOrders()

        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], 3)

    def testOpenOrderCount(self):
        self.createCustomer()
        self.createPaymentType()

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 0)

        self.createOrders()
        
        Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-22T14:42:51.221420Z"
        )

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 2)

    def testMultipleOpenOrderQuery(self):
        self.createCustomer()
        self.createPaymentType()

        Customer.objects.create(
            user_id=2, address="111 test road", phone_number="5555555555"
        )
        
        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 0)

        self.createOrders()
        
        Order.objects.create(
            customer_id=2,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        
        Order.objects.create(
            customer_id=2,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        
        response = self.client.get('/customers', {"multiple_open": True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
  
    def testListCustomer(self):
        self.createCustomer()
        
        response = self.client.get(
            '/customers'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def testGetCustomer(self):
        self.createCustomer()
        
        response = self.client.get(
            '/customers'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["address"], "111 test road")

    def testEditCustomer(self):
        self.createCustomer()
        
        updated_customer = {
            "address": "New Address",
            "phone_number": "4455555555"
        }
        
        response = self.client.put(
            reverse('customer-detail', kwargs={'pk': 1}),
            updated_customer,
            content_type="application/json",
            HTTP_AUTHORIZATION='Token ' + str(self.token_1)
        )
        
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(
            reverse('customer-detail', kwargs={'pk': 1}),
            HTTP_AUTHORIZATION='Token ' + str(self.token_1)
        )
        
        self.assertEqual(response.data["phone_number"], updated_customer["phone_number"])

if __name__ == '__main__':
    unittest.main()
