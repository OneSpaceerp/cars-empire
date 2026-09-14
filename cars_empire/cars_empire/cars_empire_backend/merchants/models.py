# merchants/models.py

from django.db import models
from django.conf import settings # To reference the custom User model
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL, verbose_name='Parent')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Merchant(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='merchants/logos/', null=True, blank=True)
    address_text = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    # Categories
    categories = models.ManyToManyField(Category, related_name='merchants', blank=True)
    makes = models.ManyToManyField('cars.CarMake', related_name='merchants', blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    tiktok_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    
    # Business Hours
    opening_hours = models.JSONField(default=dict, blank=True, null=True)
    
    # Additional Info
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=1000, help_text="Lower numbers appear first on the merchants page.")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['display_order', '-is_featured', '-rating', 'name']

class MerchantImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('cover', 'Cover Image'),
        ('gallery', 'Gallery Image'),
        ('logo', 'Logo'),
    ]

    merchant = models.ForeignKey(Merchant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='merchants/images/')
    caption = models.CharField(max_length=200, blank=True)
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES, default='gallery')
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['image_type', 'order', '-is_primary', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['merchant', 'image_type'],
                condition=models.Q(is_primary=True),
                name='unique_primary_image_per_type_per_merchant'
            )
        ]

    def save(self, *args, **kwargs):
        # If this image is set as primary, unset any other primary images of the same type
        if self.is_primary:
            MerchantImage.objects.filter(
                merchant=self.merchant,
                image_type=self.image_type,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.merchant.name} - {self.get_image_type_display()} - {self.caption or 'Image'}"

class Branch(models.Model):
    merchant = models.ForeignKey(Merchant, related_name='branches', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address_text = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.merchant.name} - {self.name}"

    class Meta:
        ordering = ['-is_main', 'name']
        verbose_name_plural = 'Branches'

class MerchantUser(models.Model):
    merchant = models.ForeignKey(Merchant, related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('staff', 'Staff')
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.merchant.name} - {self.user.get_full_name() or self.user.username}"

    class Meta:
        unique_together = ['merchant', 'user']
        ordering = ['merchant', 'role']

class Service(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(help_text="Estimated duration of the service")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['merchant__name', 'name']

    def __str__(self):
        return f"{self.merchant.name if self.merchant else 'Unassigned'} - {self.name}"

class PageAdvert(models.Model):
    PAGE_TYPE_CHOICES = [
        ('home', 'Home'),
        ('category', 'Category'),
        ('merchant', 'Merchant'),
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPE_CHOICES)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_page_type_display()} Advert: {self.title or self.id}"

class PageAdvertImage(models.Model):
    advert = models.ForeignKey(PageAdvert, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='adverts/images/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.advert} (Order {self.order})"

class PageAdvertVideo(models.Model):
    advert = models.ForeignKey(PageAdvert, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='adverts/videos/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Video for {self.advert} (Order {self.order})"

