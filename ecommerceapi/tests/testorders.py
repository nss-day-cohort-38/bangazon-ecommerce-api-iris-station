from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip


class TestOrders(TestCase):

    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user_id=1, address="111 test road", phone_number="5555555555")
        self.paymenttype = PaymentType.objects.create(
            merchant_name= "Merchant Name", 
            account_number="123456789",
            expiration_date="2028-02-18",
            customer_id=1,
            created_at="2020-05-27 14:22:22.995592"
        )

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

    def testMultipleOrders(self):
        order_one = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )
        order_two = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/orders', {'open_count': 'customer', "open": "True"})

        self.assertEqual(response.data[0]["open_count"], 2)

    def testOpenOrders(self):
        order_one = Order.objects.create(
            customer_id=1,
            payment_type_id=1,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        order_two = Order.objects.create(
            customer_id=1,
            payment_type_id=None,
            created_at="2020-05-29T14:42:51.221420Z"
        )

        response = self.client.get('/orders', {"open": "True"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 2)


if __name__ == '__main__':
    unittest.main()
