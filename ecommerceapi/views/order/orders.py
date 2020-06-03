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
from django.db.models import Count, F, When, Case, IntegerField


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field="id"
        )
        fields = ('id', 'address')
        depth = 1


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    '''
        This funciton serializes an array from the db and turns it into JSON :D
    '''
    payment_type = PaymentSerializer('payment_type')
    customer = CustomerSerializer('customer')
    open_count = serializers.SerializerMethodField()

    def get_open_count(self, obj):
        return (obj.open_count if hasattr(obj, "open_count") else None)

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='orders',
            lookup_field="id"
        )

        fields = ('id', 'payment_type_id', 'created_at',
                  'payment_type', "customer", "open_count")


class Orders(ViewSet):

    def list(self, request):
        '''
        This function returns all of the orders associated with the current user, (based of token). It is important to note that it is ordered
        by date so the first item returned is the most recent and if that payment type id is null than it is an open cart
        '''
        open = self.request.query_params.get('open', None)
        open_count = self.request.query_params.get('open_count', None)

        customer = None
        if hasattr(request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        orders = Order.objects.all()
        if customer is not None:
            orders = orders.filter(customer=customer)

        if open is not None:
            orders = orders.filter(payment_type__isnull=True)

        if open_count is not None:
            newDict = {}
            for order in orders:
                customer_id = order.customer.id
                if customer_id in newDict:
                    newDict[customer_id] += 1
                else:
                    newDict[customer_id] = 1
                    
            whens = [
                When(customer=k, then=v) for k, v in newDict.items()
            ]

            orders = orders.annotate(open_count=Case(
                *whens, default=0, output_field=IntegerField())).filter(open_count__gt=1)

        paymentType = self.request.query_params.get('payment_type_id', None)

        if paymentType is not None:
            orders.filter(payment_type_id=paymentType)
        serializer = OrderSerializer(
            orders, many=True, context={'request': request})

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
