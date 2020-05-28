'''
A django page to handle all order fetch calls

'''
from django.http import HttpResponseServerError
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order, Customer

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    '''
        This funciton serializes an array from the db and turns it into JSON :D
    '''
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'orders',
            lookup_field = "id"
        )
        fields = ('id', 'payment_type_id', 'created_at')
        depth = 1
    

class Orders(ViewSet):
    
    def list(self, request):

        '''
        This function returns all of the orders associated with the current user, (based of token). It is important to note that it is ordered
        by date so the first item returned is the most recent and if that payment type id is null than it is an open cart
        '''

        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.all()
        orders = orders.filter(customer = customer)
        paymentType = self.request.query_params.get('payment_type_id', None)
        if paymentType is not None:
            orders.filter(payment_type_id = paymentType)
        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)
    
    def create(self, request):
        '''
            Handles creating a new order when a user hits add to cart
        '''
        customer = Customer.objects.get(user=request.auth.user)
        date = datetime.datetime.now()
        newOrder = Order()
        newOrder.customer = customer
        newOrder.created_at = date
        newOrder.payment_type_id = None

        newOrder.save()

        serialize = OrderSerializer(newOrder, context={'request': request})
        return Response(serialize.data)
    




    