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
        # just customer
        fields = ('id', 'address', 'phone_number', 'user_id', "user",)

        # just user
        # fields = ('first_name', 'last_name', "last_login", "username", "email", "date_joined", "customer")
        
        # depth = 2
        
class Customers(ViewSet):
    """customer for Bangazon"""
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            # TODO: Getting the customer from the auth token 
            # may not be the best way to go 
            # if we end up using this as a global profile
            
            ## TODO: user = UserSerializer()
            ## https://stackoverflow.com/questions/20633313/django-rest-framework-get-related-model-field-in-serializer 
            customer = Customer.objects.get(pk=pk) 
            # user = User.objects.get(pk=customer.user_id)
            # customer = Customer.objects.get(user=request.data[""])
            
            # customer.user = user
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)