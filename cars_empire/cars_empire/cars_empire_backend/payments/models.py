# payments/models.py

from django.db import models
from django.conf import settings # To reference the custom User model
from django.utils import timezone

class PaymentTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    )

    # Link to user who initiated the payment
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_transactions')
    # Link to an Order model if multiple coupons bought at once, or leave null if linking directly from Coupon
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name="transactions")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit_card')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    payment_details = models.JSONField(null=True, blank=True)  # Store payment gateway specific details
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Optional: Store raw callback data from Paymob for debugging/auditing
    # raw_callback_data = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_id} - {self.amount} {self.currency}"

    def mark_as_completed(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message=None):
        self.status = 'failed'
        self.error_message = error_message
        self.save()

    def mark_as_refunded(self):
        self.status = 'refunded'
        self.save()

