'''
A django page to handle all product type fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import ProductType, Product




class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttypes',
            lookup_field='id'
        )
        fields = ('id', 'name', )
        depth = 1

class ProductTypes(ViewSet):

    '''' a class to handle all the product types viewset

    Arguments:
        ViewSet '''

    def create(self, request):
        ''' Handle POST operations and returns JSON serialized product type instance'''

        newproducttype = ProductType()
        newproducttype.name = request.data["name"]
        newproducttype.save()

        serializer = ProductTypeSerializer(newproducttype, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        home = self.request.query_params.get('number', None)
        if home is not None:
            producttypes = ProductType.objects.all()[:20]
        else:
             producttypes = ProductType.objects.all()

        serializer = ProductTypeSerializer(producttypes, many=True, context={"request": request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        producttype = ProductType.objects.get(pk=pk)
        serializer = ProductTypeSerializer(producttype, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None): 
        pass

    def destroy(self, request, pk=None):
        pass
