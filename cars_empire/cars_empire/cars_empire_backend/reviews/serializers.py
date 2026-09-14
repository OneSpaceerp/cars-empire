from rest_framework import serializers
from .models import CarReview, MerchantReview

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        fields = [
            'id', 'user', 'rating', 'title', 'content',
            'created_at', 'updated_at', 'is_verified', 'is_public'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'is_verified']

class CarReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = CarReview
        fields = ReviewSerializer.Meta.fields + ['car']

class MerchantReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = MerchantReview
        fields = ReviewSerializer.Meta.fields + ['merchant'] 