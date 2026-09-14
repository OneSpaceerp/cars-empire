from rest_framework import serializers
from .models import Deal, DealImage, DealAnalytics, UserBehavior, DealAlert, Notification
from merchants.models import Category
from merchants.serializers import MerchantSerializer
from cars.serializers import CarModelSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent']
        read_only_fields = ['slug']

class DealImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealImage
        fields = ['image', 'alt_text']

class DealSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    images = DealImageSerializer(many=True, read_only=True)
    merchant = MerchantSerializer(read_only=True)
    applicable_models = CarModelSerializer(many=True, read_only=True)
    discount_percentage = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Deal
        fields = [
            'id', 'title', 'slug', 'description', 'original_price',
            'discount_price', 'discount_percentage', 'start_datetime', 'end_datetime',
            'quantity_limit', 'terms_and_conditions',
            'redemption_instructions', 'status', 'category',
            'category_id', 'created_at', 'updated_at', 'is_featured',
            'images', 'merchant', 'applicable_models', 'deal_type',
            'urgency_level', 'views_count', 'clicks_count', 'purchases_count',
            'is_trending', 'is_flash_sale', 'is_active'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'views_count', 'clicks_count', 'purchases_count']

class DealAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealAnalytics
        fields = ['date', 'views', 'clicks', 'purchases', 'conversion_rate', 'revenue']

class UserBehaviorSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only=True)
    
    class Meta:
        model = UserBehavior
        fields = ['id', 'deal', 'action', 'timestamp']

class DealAlertSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    car_models = CarModelSerializer(many=True, read_only=True)
    
    class Meta:
        model = DealAlert
        fields = [
            'id', 'keywords', 'categories', 'car_models',
            'price_range_min', 'price_range_max', 'location_radius',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    deal = DealSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'deal', 'is_read', 'created_at'
        ]
        read_only_fields = ['created_at'] 