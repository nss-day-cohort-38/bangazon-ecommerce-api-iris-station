"""View module for handling requests about attractions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ecommerceapi.models import PaymentType


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Attractions

    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='payment_types',
            lookup_field='id'
        )

        fields = ('id', 'merchant_name', "account_number",
                  "expiration_date", "customer_id", "created_at")
