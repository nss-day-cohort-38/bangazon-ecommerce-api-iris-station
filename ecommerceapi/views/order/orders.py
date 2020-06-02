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
from .. import PaymentSerializer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name = 'customer',
            lookup_field = "id"
        )
        fields = ('id', 'address')
        depth = 1

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    '''
        This funciton serializes an array from the db and turns it into JSON :D
    '''
    payment_type = PaymentSerializer('payment_type')
    customer = CustomerSerializer('customer')
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name = 'orders',
            lookup_field = "id"
        )

        fields = ('id', 'payment_type_id', 'created_at', 'payment_type', "customer")
    

class Orders(ViewSet):
    
    def list(self, request):

        '''
        This function returns all of the orders associated with the current user, (based of token). It is important to note that it is ordered
        by date so the first item returned is the most recent and if that payment type id is null than it is an open cart
        '''
        customer = None
        if hasattr( request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        orders = Order.objects.all()
        if customer is not None:
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
    

    def update(self, request, pk=None):

        ogOrder = Order.objects.get(pk=pk)
        ogOrder.payment_type_id = request.data['payment_type_id']

        ogOrder.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):

        try:
            ogOrder = Order.objects.get(pk=pk)
            ogOrder.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        # except Order.DoesNotExist as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    