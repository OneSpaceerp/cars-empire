from django.db import models
from django.conf import settings
from merchants.models import Merchant
from deals.models import Deal

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    # Temporarily comment out service field
    # service = models.ForeignKey('merchants.Service', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x item from {self.merchant.name}"

    @property
    def total_price(self):
        if self.deal and hasattr(self.deal, 'discount_price'):
            return self.deal.discount_price * self.quantity
        elif self.deal and hasattr(self.deal, 'price'):
            return self.deal.price * self.quantity
        return 0

    class Meta:
        unique_together = ['cart', 'deal'] 