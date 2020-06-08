from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import PaymentType, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

class TestPaymentTypes(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        self.username = "TestUser"
        self.password = "testword1"
        self.user =  User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user_id=1, address="111 test road", phone_number="5555555555")

    def testPost(self):
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")

        response = self.client.get(
            reverse('paymenttypes-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["merchant_name"], "Stupid Company")
    
    def testList(self):
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")

        response = self.client.get(
            reverse('paymenttypes-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(len(response.data), 1)
        

    def testGet(self):
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")

        response = self.client.get(
            reverse('paymenttypes-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]["id"], 1)

        self.assertIn(pt.merchant_name.encode(), response.content)


    def testDelete(self):
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")

        response = self.client.delete(
            reverse('paymenttypes-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        self.assertEqual(response.status_code, 204)

        response = self.client.get(
            reverse('paymenttypes-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(len(response.data), 0)



if __name__ == '__main__':
    unittest.main()
