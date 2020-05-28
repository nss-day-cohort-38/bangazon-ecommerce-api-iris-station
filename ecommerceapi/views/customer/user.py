from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import Customer
from django.contrib.auth.models import User
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for users

    Arguments:
        serializers
    """
    class Meta:
        model = User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field='id'
        )
        
        fields = ('first_name', 'last_name', "last_login", "username", "email", "date_joined",)
        
class Users(ViewSet):
    """user for Bangazon"""
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            user = User.objects.get(pk=pk)             
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def update(self, request, pk=None):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(pk=pk)
        user.username = request.data["username"]
        user.password = request.data["password"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.save()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
