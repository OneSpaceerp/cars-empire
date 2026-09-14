from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import User, Vehicle, Order, OrderItem
from deals.models import Deal
from cars.models import CarMake, CarModel
import re

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)
    phone = serializers.CharField(required=True, max_length=15)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone', 'first_name', 'last_name', 'password', 're_password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True},
            'username': {'required': True}
        }

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and @/./+/-/_ characters."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_password'):
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        attrs.pop('re_password', None)
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('date_joined',)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('username', 'email', 'date_joined')

class VehicleSerializer(serializers.ModelSerializer):
    make_id = serializers.PrimaryKeyRelatedField(source='make', queryset=CarMake.objects.all())
    make_name = serializers.CharField(source='make.name', read_only=True)
    model_id = serializers.PrimaryKeyRelatedField(source='model', queryset=CarModel.objects.all())
    model_name = serializers.CharField(source='model.name', read_only=True)
    class Meta:
        model = Vehicle
        fields = ['id', 'make_id', 'make_name', 'model_id', 'model_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'make_name', 'model_name']

class OrderItemSerializer(serializers.ModelSerializer):
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'deal', 'deal_title', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'items'] 