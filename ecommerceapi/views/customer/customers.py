""" Customer for Bangazon Ecommerce"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer, Order
from django.contrib.auth.models import User
from django.db.models import Count, F, When, Case, IntegerField, Q



class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer

    Arguments:
        serializers
    """
    # Will hold the value of how many orders a customer has (open and closed)
    order_count = serializers.SerializerMethodField()

    # Will hold the value of how many open orders a customer has
    open_order_count = serializers.SerializerMethodField()

    def get_order_count(self, obj):
        return (obj.order_count if hasattr(obj, "order_count") else None)

    def get_open_order_count(self, obj):
        return (obj.open_order_count if hasattr(obj, "open_order_count") else None)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'address', 'phone_number', 'user_id',
                  'user', "order_count", "open_order_count")

        depth = 1


class Customers(ViewSet):
    """customer for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            # if customer id is in the url
            customer = Customer.objects.get(pk=pk)

            serializer = CustomerSerializer(
                customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to customers resource. 
        Used when the user is extracted from the token

        Returns:
            Response -- JSON serialized list (of one customer)
        """

        try:
            many = True
            customer = Customer.objects.all()
            multiple_open = self.request.query_params.get('multiple_open', None)

            # Adds order_count and oopen_order_count to api object
            customer = customer.annotate(order_count=Count("order")).annotate(open_order_count=Count('order', filter=Q(order__payment_type=None)))

            # Filter to only show customers with multiple open orders   
            if multiple_open is not None:
                customer = customer.filter(open_order_count__gt=1)

            if hasattr(request.auth, "user"):
                many = False
                customer = customer.get(user=request.auth.user)

            serializer = CustomerSerializer(
                customer, many=many, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a customer

        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=pk)
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

