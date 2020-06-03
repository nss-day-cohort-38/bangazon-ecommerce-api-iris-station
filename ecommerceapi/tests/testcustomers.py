from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip


class TestCustomers(TestCase):

    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.paymenttype = PaymentType.objects.create(
            merchant_name="Merchant Name",
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )


    def testOrderCount(self):
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], None)

        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], 2)

    def testOpenOrderCount(self):
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], None)

        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 1)



if __name__ == '__main__':
    unittest.main()
