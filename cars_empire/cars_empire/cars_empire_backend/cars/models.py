# cars/models.py

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from merchants.models import Category # Import Category from merchants app

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    icon = models.ImageField(upload_to='car_makes/icons/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    year_start = models.PositiveSmallIntegerField(null=True, blank=True)
    year_end = models.PositiveSmallIntegerField(null=True, blank=True) # Null if still in production
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    icon = models.ImageField(upload_to='car_models/icons/', null=True, blank=True)

    class Meta:
        unique_together = (("make", "name", "year_start", "year_end"))
        ordering = ["make__name", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.make.name}-{self.name}")
            # Handle potential year range in slug if needed for uniqueness, though unique_together should suffice
            self.slug = base_slug
            # Add logic here if needed to ensure slug uniqueness if base_slug isn't unique
        super().save(*args, **kwargs)

    def __str__(self):
        year_start_str = self.year_start or ""
        year_end_str = self.year_end or "Present"
        years = f"({year_start_str} - {year_end_str})"
        return f"{self.make.name} {self.name} {years if self.year_start else ''}"

class Car(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name