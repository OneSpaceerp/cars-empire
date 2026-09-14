# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Set username to email if not provided
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    # Inherits first_name, last_name, email, password, etc.
    # Add custom fields if needed, e.g.:
    # email_verified = models.BooleanField(default=False)
    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email or self.phone or self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # phone_number field removed, now on User
    # Add other profile fields like profile picture, default address etc.
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create/update UserProfile when User is created/saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class UserCar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    car_model = models.ForeignKey('cars.CarModel', on_delete=models.PROTECT) # Protect car model data
    year = models.PositiveSmallIntegerField()
    vin = models.CharField(max_length=17, blank=True, null=True) # Vehicle Identification Number
    registration_plate = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        unique_together = (("user", "car_model", "year")) # Prevent duplicate cars per user
        ordering = ["-id"] # Show newest first

    def __str__(self):
        return f"{self.user.username}\'s {self.year} {self.car_model.make.name} {self.car_model.name}"

class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    make = models.ForeignKey('cars.CarMake', on_delete=models.PROTECT)
    model = models.ForeignKey('cars.CarModel', on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    license_plate = models.CharField(max_length=32, blank=True, default='')
    mileage_km = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.CharField(
        max_length=20, 
        blank=True, 
        default='petrol',
        choices=[
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('hybrid', 'Hybrid'),
            ('electric', 'Electric'),
        ]
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        year_str = f" {self.year}" if self.year else ""
        plate_str = f" ({self.license_plate})" if self.license_plate else ""
        return f"{self.make.name} {self.model.name}{year_str}{plate_str}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    )
    order_number = models.CharField(max_length=32, unique=True, blank=True, null=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    currency = models.CharField(max_length=3, default='EGP')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wallet_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text='Grand total payable')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment', db_index=True)
    payment_transaction = models.ForeignKey(
        'payments.PaymentTransaction', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders'
    )
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            rand_str = ''.join(random.choices('0123456789ABCDEF', k=6))
            self.order_number = f"CE-{date_str}-{rand_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number or self.id} ({self.get_status_display()}) - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    deal = models.ForeignKey('deals.Deal', on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    branch = models.ForeignKey('merchants.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Unit price
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_required = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.line_total:
            self.line_total = (self.price * self.quantity) - self.discount_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.deal.title} (Order #{self.order.order_number or self.order.id})"