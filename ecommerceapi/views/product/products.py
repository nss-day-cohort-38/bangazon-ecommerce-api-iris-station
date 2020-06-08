'''
A django page to handle all product fetch calls

'''
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.files.base import ContentFile
from ecommerceapi.models import Product, Customer, OrderProduct, ProductType
from datetime import datetime
from django.http import HttpResponse
import json
from django.utils import timezone



class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttypes',
            lookup_field='id'
        )
        fields = ('id', 'name',)
        depth = 1



class ProductSerializer(serializers.HyperlinkedModelSerializer):

    product_type = ProductTypeSerializer('product_type')
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='products',
            lookup_field='id'
        )
        fields = ('id', 'title', 'price', 'description', 'quantity', "location",
                  'created_at', 'image_path', 'product_type_id', 'amount_sold', 'product_type')
        depth = 1


class Products(ViewSet):

    '''' a class to handle all the products viewset

    Arguments:
        ViewSet '''

    def create(self, request):
        ''' Handle POST operations and returns JSON serialized product instance'''

        newproduct = Product()
        newproduct.title = request.data["title"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        # Keith:
        # If a user is uploading a file, 
        # assign it, otherwise skip this and allow it to be null
        if request.FILES:
        # "When Django handles a file upload, the file data ends up placed in request.FILES"
        # https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
            newproduct.image_path = request.FILES["image_path"]
        
        # https://stackoverflow.com/a/37607525/798303
        # Changed to timezone (from datetime) to fix a naive time error
        newproduct.created_at = timezone.now()
        newproduct.product_type_id = request.data["product_type_id"]
        newcustomer = Customer.objects.get(user=request.auth.user)
        newproduct.customer = newcustomer
        newproduct.save()

        serializer = ProductSerializer(
            newproduct, context={'request': request})

        return Response(serializer.data)

    def list(self, request):
        ''' handles get requests to server and returns a JSON response'''
        home = self.request.query_params.get('number', None)
        if home is not None:
            products = Product.objects.all()[:20]
        else:
            products = Product.objects.all()

        ''' handles the My Products list for each user '''
        user = self.request.query_params.get('user', None)
        if hasattr(request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        if user is not None:
            products = products.filter(customer_id=customer.id)

        # handles fetching list of all products of a certain product type
        product_type_id = self.request.query_params.get('productTypeId', None)
        if product_type_id is not None:
            products = products.filter(product_type_id=product_type_id)

        # this loop will count how many products are in the order_product table specifically ones where the paymenttypeid is not null
        # meaning the user has paid for the product.
        for product in products:

            productsSold = OrderProduct.objects.raw('''SELECT
            op.id opId,
            op.order_id,
            op.product_id,
            o.id,
            o.created_at
            from ecommerceapi_orderproduct op
            left join ecommerceapi_order o on  op.order_id = o.id
            where o.payment_type_id Not NULL and product_id = %s
            order by product_id''',
                [product.id])

            count = len(list(productsSold))
            product.amount_sold = count

        serializer = ProductSerializer(
            products, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''handles fetching ony one product'''
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(json.dumps({"error": "Does Not Exist"}), content_type="application/json")

    def update(self, request, pk=None):

        ogProduct = Product.objects.get(pk=pk)
        ogProduct.quantity = request.data['quantity']

        ogProduct.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        '''handles delete product'''
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
