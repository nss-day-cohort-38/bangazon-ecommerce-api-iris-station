"""View module for handling requests about attractions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from saturdayintheparkapi.models import Attraction, ParkArea

class Payments(ViewSet):
    """Payments for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payments instance
        """
        pass


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
        pass
