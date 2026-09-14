from rest_framework import serializers
from .models import Cart, CartItem
from merchants.serializers import MerchantSerializer  # Temporarily remove ServiceSerializer
from deals.models import Deal

class CartItemSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(read_only=True)
    # Temporarily comment out service field
    # service = ServiceSerializer(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    deal_id = serializers.PrimaryKeyRelatedField(source='deal', queryset=Deal.objects.all(), required=False, allow_null=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'merchant', 'deal_id', 'quantity', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user', 'items', 'total_items', 'total_price'] 