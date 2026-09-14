# reviews/models.py

from django.db import models
from django.conf import settings # To reference the custom User model
from deals.models import Deal # Import from deals app
# from coupons.models import Coupon # Optional: Link to coupon for verification
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class CarReview(Review):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_reviews')
    car = models.ForeignKey('cars.CarModel', on_delete=models.CASCADE, related_name='reviews')

class MerchantReview(Review):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='merchant_reviews')
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.CASCADE, related_name='reviews')

# Temporarily comment out ServiceReview model
# class ServiceReview(Review):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_reviews')
#     service = models.ForeignKey('merchants.Service', on_delete=models.CASCADE, related_name='reviews')

