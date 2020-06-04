from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip


class TestCustomers(TestCase):

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
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], 0)

        PaymentType.objects.create(
            merchant_name="Merchant Name",
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

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

        new_order = Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["order_count"], 3)

    def testOpenOrderCount(self):
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

        PaymentType.objects.create(
            merchant_name="Merchant Name",
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 0)

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

        Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 2)

    def testMultipleOpenOrderFilter(self):
        Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")

        PaymentType.objects.create(
            merchant_name="Merchant Name",
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        Customer.objects.create(
            user_id=2, address="111 test road", phone_number="5555555555")

        response = self.client.get('/customers')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["open_order_count"], 0)

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
            customer_id=2,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/customers', {"multiple_open": True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


if __name__ == '__main__':
    unittest.main()
