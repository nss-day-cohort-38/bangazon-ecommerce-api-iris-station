'''
A django page to handle all order fetch calls

'''
from django.http import HttpResponseServerError
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Order, Customer, Product, OrderProduct

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
            model = Product
            url = serializers.HyperlinkedIdentityField(
                view_name='products',
                lookup_field='id'
            )
            fields = ('id', 'title', 'price', 'description', 'quantity', "location", 'created_at', 'image_path', 'product_type_id', 'deleted')
    

class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    '''
        This funciton serializes an array from the db and turns it into JSON :D
    '''
    product = ProductSerializer('product')

    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name = 'order_products',
            lookup_field = "id"
        )
        fields = ('id', 'order_id', 'product')
    

    """JSON serializer for products

    Arguments:
        serializers
    """
class OrderProducts(ViewSet):
    
    def list(self, request):

        '''
        This function returns all of the order-product relationships and has the option to filter by order number
        '''

        order_products = OrderProduct.objects.all()
        order_id = self.request.query_params.get('order_id', None)
        if order_id is not None:
            order_products = order_products.filter(order_id = order_id)
        serializer = OrderProductSerializer(order_products, many=True, context={'request': request})

        return Response(serializer.data)
    
    def create(self, request):

        new_order_product = OrderProduct()
        new_order_product.order_id =  request.data["order_id"]
        new_order_product.product_id =  request.data["product_id"]
        new_order_product.save()

        serializer = OrderProductSerializer(new_order_product, context={'request': request})
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        try:
            orderProduct = OrderProduct.objects.get(pk=pk)
            orderProduct.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

