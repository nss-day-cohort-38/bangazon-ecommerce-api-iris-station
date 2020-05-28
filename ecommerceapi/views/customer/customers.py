""" Customer for Bangazon Ecommerce"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer
from django.contrib.auth.models import User

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer

    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'address', 'phone_number', 'user_id', 'user',)
        
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

            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)