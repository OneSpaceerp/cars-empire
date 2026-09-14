from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PaymentTransaction
from .serializers import PaymentTransactionSerializer

# Create your views here.

class PaymentTransactionListView(generics.ListCreateAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentTransactionDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)

class PaymentTransactionWebhookView(generics.CreateAPIView):
    permission_classes = []  # No authentication required for webhooks
    serializer_class = PaymentTransactionSerializer

    def create(self, request, *args, **kwargs):
        # Here you would implement the webhook logic to handle payment gateway callbacks
        # This is a placeholder implementation
        return Response(
            {'message': 'Webhook received'},
            status=status.HTTP_200_OK
        )
