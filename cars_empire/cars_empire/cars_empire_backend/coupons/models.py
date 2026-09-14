# coupons/models.py

import uuid
import hashlib
import random
import string
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator
from deals.models import Deal

class Coupon(models.Model):
    """
    Authoritative unique customer service entitlement voucher (Waffarha model).
    Each purchased quantity of a deal results in exactly ONE Coupon with a globally unique code and QR token.
    """
    STATUS_CHOICES = (
        ("available", "Available"),   # Issued and ready to be redeemed
        ("validated", "Validated"),   # Looked up / verified by merchant
        ("redeeming", "Redeeming"),   # Concurrency lock held during checkout at workshop
        ("redeemed", "Redeemed"),     # Service performed & voucher consumed
        ("expired", "Expired"),       # Passed validity date
        ("cancelled", "Cancelled"),   # Cancelled before redemption
        ("refunded", "Refunded"),     # Refund processed
        ("suspended", "Suspended"),   # On hold / dispute
        # Legacy status mapping
        ("issued", "Issued (Available)"),
    )

    # Entitlement links
    deal = models.ForeignKey(Deal, on_delete=models.PROTECT, related_name="coupons")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coupons", verbose_name="Customer")
    order = models.ForeignKey('users.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name="coupons")
    order_item = models.ForeignKey('users.OrderItem', on_delete=models.SET_NULL, null=True, blank=True, related_name="coupons")
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.CASCADE, null=True, blank=True, related_name="issued_coupons")
    branch = models.ForeignKey('merchants.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name="branch_coupons")
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True, blank=True, related_name="vehicle_coupons")

    # Cryptographic unique identifiers
    coupon_code = models.CharField(max_length=50, unique=True, editable=False, db_index=True)
    code_hash = models.CharField(max_length=64, blank=True, db_index=True, help_text="SHA-256 hash for fast secure lookup")
    qr_token = models.CharField(max_length=64, unique=True, null=True, blank=True, db_index=True, help_text="Cryptographically secure opaque token for QR code")

    # State & Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available", db_index=True)
    issued_at = models.DateTimeField(default=timezone.now)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    purchase_datetime = models.DateTimeField(auto_now_add=True)
    redemption_datetime = models.DateTimeField(null=True, blank=True)
    redeemed_by_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="redeemed_coupons"
    )

    # Payment link
    payment_transaction = models.ForeignKey(
        "payments.PaymentTransaction", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="coupons"
    )

    # Backward-compatible promo fields (retained to prevent legacy migration issues)
    description = models.TextField(blank=True, default="")
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')],
        default='percentage'
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['coupon_code', 'status']),
            models.Index(fields=['qr_token', 'status']),
            models.Index(fields=['merchant', 'status', 'valid_until']),
        ]

    def save(self, *args, **kwargs):
        # Derive merchant from deal if not explicitly set
        if not self.merchant and self.deal and hasattr(self.deal, 'merchant'):
            self.merchant = self.deal.merchant

        # Set default validity from deal end_datetime if not set
        if not self.valid_until and self.deal and hasattr(self.deal, 'end_datetime'):
            self.valid_until = self.deal.end_datetime

        # Auto-generate unique coupon code if missing
        if not self.coupon_code:
            self.coupon_code = self.generate_unique_code()

        # Update SHA-256 hash of canonical code
        if self.coupon_code:
            normalized = self.coupon_code.strip().upper()
            self.code_hash = hashlib.sha256(normalized.encode('utf-8')).hexdigest()

        # Auto-generate cryptographically secure QR token if missing
        if not self.qr_token:
            self.qr_token = uuid.uuid4().hex

        super().save(*args, **kwargs)

    @classmethod
    def generate_unique_code(cls, prefix="CE"):
        """Generates a high-entropy, human-friendly unique coupon code, e.g. CE-OIL-7K4P9Q2M"""
        chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"  # Exclude easily confused characters (0, O, 1, I)
        for _ in range(10):
            random_str = "".join(random.choices(chars, k=8))
            code = f"{prefix}-{random_str[:4]}-{random_str[4:]}"
            if not cls.objects.filter(coupon_code=code).exists():
                return code
        # Fallback with uuid if collision persists
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return f"{self.coupon_code} - {self.deal.title} ({self.user.username})"

    def is_valid(self):
        """Returns True if the voucher is active and ready to be redeemed"""
        now = timezone.now()
        is_status_valid = self.status in ['available', 'issued']
        is_date_valid = (self.valid_from <= now) and (self.valid_until is None or self.valid_until >= now)
        return is_status_valid and is_date_valid

    def can_be_redeemed_at(self, merchant_id, branch_id=None):
        """Validates that this voucher belongs to the specified merchant and branch"""
        if not self.is_valid():
            return False, "Coupon is not active or has expired."
        if self.merchant_id and self.merchant_id != merchant_id:
            return False, "Coupon does not belong to this merchant."
        if self.branch_id and branch_id and self.branch_id != branch_id:
            return False, "Coupon is restricted to a specific branch."
        return True, "Valid"


class PromoCode(models.Model):
    """
    Marketing discount coupons applied at checkout (e.g. WELCOME10, SAVE50).
    Separated from purchased customer service entitlements.
    """
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    discount_type = models.CharField(
        max_length=10,
        choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')],
        default='percentage'
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    min_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Promo / Discount Code"
        verbose_name_plural = "Promo / Discount Codes"

    def __str__(self):
        return f"{self.code} ({self.discount_value}{'%' if self.discount_type == 'percentage' else ' EGP'})"

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= (self.end_date or now) and
            (self.usage_limit is None or self.times_used < self.usage_limit)
        )


class Redemption(models.Model):
    """
    Audit record of a consumed coupon at a merchant branch (PRD Section 17.3).
    Ensures single-use concurrency safety and settlement traceability.
    """
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, related_name="redemption")
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.PROTECT, related_name="redemptions")
    branch = models.ForeignKey('merchants.Branch', on_delete=models.PROTECT, null=True, blank=True, related_name="redemptions")
    staff_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="staff_redemptions"
    )
    device_fingerprint = models.CharField(max_length=255, blank=True, default='')
    redeemed_at = models.DateTimeField(default=timezone.now)
    method = models.CharField(
        max_length=20, 
        choices=[
            ('qr_scan', 'QR Code Scan'),
            ('code_entry', 'Manual Code Entry'),
            ('pos_sync', 'POS Sync'),
            ('manual', 'Admin Override'),
        ], 
        default='qr_scan'
    )
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    notes = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=20, 
        choices=[
            ('completed', 'Completed'),
            ('reversed', 'Reversed'),
            ('disputed', 'Disputed'),
        ], 
        default='completed'
    )
    reversal_reason = models.TextField(blank=True, default='')

    class Meta:
        ordering = ["-redeemed_at"]

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            date_str = timezone.now().strftime('%Y%m%d')
            rand_str = ''.join(random.choices('0123456789', k=6))
            self.receipt_number = f"CE-R-{date_str}-{rand_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Redemption #{self.receipt_number} - {self.coupon.coupon_code}"


class CouponEvent(models.Model):
    """
    Immutable audit log tracking every lifecycle change of a Coupon (PRD Section 17.3).
    """
    EVENT_CHOICES = (
        ('issued', 'Issued'),
        ('validated', 'Validated'),
        ('redeeming', 'Redemption In Progress'),
        ('redeemed', 'Redeemed'),
        ('reversed', 'Reversed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=30, choices=EVENT_CHOICES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey('merchants.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.coupon.coupon_code} - {self.event_type} at {self.created_at}"


class WorkOrder(models.Model):
    """
    Workshop operational job card created upon coupon redemption (PRD Section 2.9 & 17.3).
    Tracks vehicle service progress, mechanic assignment, and digital service history.
    """
    STATUS_CHOICES = (
        ('opened', 'Opened / Checked In'),
        ('diagnosing', 'Diagnosing'),
        ('in_progress', 'In Progress'),
        ('awaiting_parts', 'Awaiting Parts / Approval'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    work_order_number = models.CharField(max_length=50, unique=True, blank=True, db_index=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name="work_orders")
    redemption = models.OneToOneField(Redemption, on_delete=models.SET_NULL, null=True, blank=True, related_name="work_order")
    merchant = models.ForeignKey('merchants.Merchant', on_delete=models.PROTECT, related_name="work_orders")
    branch = models.ForeignKey('merchants.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name="work_orders")
    vehicle = models.ForeignKey('users.Vehicle', on_delete=models.SET_NULL, null=True, blank=True, related_name="work_orders")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_work_orders")
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_work_orders")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='opened', db_index=True)
    arrival_mileage_km = models.PositiveIntegerField(null=True, blank=True, help_text="Odometer reading when vehicle arrives")
    completion_note = models.TextField(blank=True, default='')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.work_order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            rand_str = ''.join(random.choices('0123456789ABCDEF', k=5))
            self.work_order_number = f"WO-{date_str}-{rand_str}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Work Order #{self.work_order_number} ({self.get_status_display()})"


def generate_unique_coupons_for_order(order):
    """
    Authoritative transaction helper (PRD Section 17.4 & 17.11):
    When an order is paid, transactionally mints N unique coupons (one per paid unit).
    """
    issued_coupons = []
    with transaction.atomic():
        for item in order.items.all():
            deal = item.deal
            merchant = deal.merchant
            branch = item.branch
            vehicle = item.vehicle

            for _ in range(item.quantity):
                coupon = Coupon.objects.create(
                    deal=deal,
                    user=order.user,
                    order=order,
                    order_item=item,
                    merchant=merchant,
                    branch=branch,
                    vehicle=vehicle,
                    status='available',
                    valid_from=timezone.now(),
                    valid_until=deal.end_datetime,
                    payment_transaction=order.payment_transaction,
                )
                # Audit event
                CouponEvent.objects.create(
                    coupon=coupon,
                    event_type='issued',
                    actor=order.user,
                    branch=branch,
                    notes=f"Issued from Order #{order.order_number}"
                )
                issued_coupons.append(coupon)

    return issued_coupons

