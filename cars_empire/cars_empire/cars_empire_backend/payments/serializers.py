from rest_framework import serializers
from .models import PaymentTransaction

class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'user', 'amount', 'currency', 'status',
            'payment_method', 'transaction_id', 'payment_details',
            'error_message', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = [
            'user', 'status', 'transaction_id', 'payment_details',
            'error_message', 'created_at', 'updated_at', 'completed_at'
        ] 