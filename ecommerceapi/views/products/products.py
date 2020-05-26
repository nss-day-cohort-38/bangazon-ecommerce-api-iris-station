'''
A django page to handle all product fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='products',
            lookup_field='id'
        )
        fields = ('id', 'title', 'price', 'description', 'quantity', "location", 'image_path', 'product_type_id')
        depth = 1

class Products(ViewSet):

    def create(self, request):
        pass
    
    def list(self, request):
        pass
    
    def retrieve(self, request, pk=None):
        pass
    def update(self, request, pk=None): 
        pass

    def destroy(self, request, pk=None):
        pass