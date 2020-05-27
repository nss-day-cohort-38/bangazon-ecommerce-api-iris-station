'''
A django page to handle all order fetch calls

'''
from django.http import HttpResponseServerError
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
    

class Orders(ViewSet):
    
    def list(self, request):

        customer = Customer.objects.get(user=request.auth.user)
        orders = Order.objects.all()
        orders = orders.filter(customer = customer)
        paymentType = self.request.query_params.get('payment_type_id', None)
        if paymentType is not None:
            orders.filter(payment_type_id = paymentType)
        serializer = OrderSerializer(orders, many=True, context={'request': request})

        return Response(serializer.data)


    