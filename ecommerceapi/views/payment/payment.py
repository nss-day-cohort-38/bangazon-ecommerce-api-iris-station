"""View module for handling requests about attractions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.utils import timezone

from ecommerceapi.models import PaymentType, Customer
from .paymentserializer import PaymentSerializer
from datetime import datetime
from rest_framework.authtoken.models import Token


class Payments(ViewSet):
    """Payments for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payments instance
        """
        data = request.data
        now = datetime.now(tz=timezone.utc)
        user_id = request.user.id
        new_payment = PaymentType.objects.create(
            merchant_name=data["merchant_name"],
            account_number=data["account_number"],
            expiration_date=data["expiration_date"],
            customer=Customer.objects.get(user__id=user_id),
            created_at=now
        )

        serializer = PaymentSerializer(
            new_payment, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Payments

        Returns:
            Response -- JSON serialized Payments instance
        """
        pass

    def update(self, request, pk=None):
        """Handle PUT requests for a Payments

        Returns:
            Response -- Empty body with 204 status code
        """
        pass

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Payments

        Returns:
            Response -- 200, 404, or 500 status code
        """
        pass

    def list(self, request):
        """Handle GET requests to Payments resource

        Returns:
            Response -- JSON serialized list of Payments
        """
        payments = PaymentType.objects.all()

        attraction = self.request.query_params.get("attraction", None)
        customer = None
        if hasattr(request.auth, "user"):
            customer = Customer.objects.get(user=request.auth.user)

        if customer is not None:
            payments = PaymentType.objects.filter(customer__id=customer.id)

        serializer = PaymentSerializer(
            payments, many=True, context={'request': request})

        return Response(serializer.data)
