# deals/models.py

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings # To reference the custom User model
from cars.models import CarModel # Import from cars app
from merchants.models import Merchant, Category # Import Category from merchants app

class Deal(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("active", "Active"), # Approved and visible
        ("inactive", "Inactive"), # Temporarily hidden by merchant/admin
        ("expired", "Expired"), # Past end_datetime
    )
    
    DEAL_TYPE_CHOICES = (
        ("service", "Service Deal"),
        ("product", "Product Deal"),
        ("rental", "Rental Deal"),
        ("sale", "Sale Deal"),
        ("maintenance", "Maintenance Deal"),
    )
    
    URGENCY_LEVEL_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("flash", "Flash Sale"),
    )
    
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="deals")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="deals")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField()
    quantity_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Max number of coupons that can be sold for this deal")
    terms_and_conditions = models.TextField()
    redemption_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    
    # Enhanced fields
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES, default="service")
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVEL_CHOICES, default="medium")
    views_count = models.PositiveIntegerField(default=0)
    clicks_count = models.PositiveIntegerField(default=0)
    purchases_count = models.PositiveIntegerField(default=0)
    is_trending = models.BooleanField(default=False)
    is_flash_sale = models.BooleanField(default=False)
    flash_sale_duration = models.DurationField(null=True, blank=True, help_text="Duration for flash sales")
    
    # *** Crucial Field for Car Specificity ***
    applicable_models = models.ManyToManyField(
        CarModel, 
        blank=True, 
        related_name="deals", 
        help_text="Select specific car models this deal applies to. Leave blank if universally applicable within category."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Add logic to ensure slug uniqueness, e.g., appending ID or timestamp if needed
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        return self.status == "active" and self.start_datetime <= now and self.end_datetime >= now

    @property
    def discount_percentage(self):
        if self.original_price and self.discount_price and self.original_price > 0:
            return round(((self.original_price - self.discount_price) / self.original_price) * 100)
        return 0

class DealImage(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="deal_images/")
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Image for {self.deal.title}"

class DealAnalytics(models.Model):
    """Track deal performance metrics"""
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="analytics")
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)
    conversion_rate = models.FloatField(default=0.0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['deal', 'date']
        ordering = ['-date']

class UserBehavior(models.Model):
    """Track user interactions with deals"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="behaviors")
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name="user_behaviors")
    action = models.CharField(max_length=50, choices=[
        ('view', 'View'),
        ('click', 'Click'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('share', 'Share'),
        ('save', 'Save'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']

class DealAlert(models.Model):
    """User alerts for specific deal criteria"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="deal_alerts")
    keywords = models.CharField(max_length=200, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    car_models = models.ManyToManyField(CarModel, blank=True)
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location_radius = models.PositiveIntegerField(default=50, help_text="Radius in kilometers")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

class Notification(models.Model):
    """User notifications system"""
    NOTIFICATION_TYPES = (
        ('deal_alert', 'Deal Alert'),
        ('price_drop', 'Price Drop'),
        ('new_deal', 'New Deal'),
        ('deal_expiring', 'Deal Expiring'),
        ('purchase_confirmation', 'Purchase Confirmation'),
        ('general', 'General'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

