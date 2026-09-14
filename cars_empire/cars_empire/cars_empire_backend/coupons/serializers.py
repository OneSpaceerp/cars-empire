from rest_framework import serializers
from .models import Coupon, PromoCode, Redemption, CouponEvent, WorkOrder
from deals.serializers import DealSerializer
import io
import base64

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    qr_code_image = serializers.SerializerMethodField()
    deal_title = serializers.CharField(source='deal.title', read_only=True)
    merchant_name = serializers.CharField(source='merchant.name', read_only=True, default='')
    branch_name = serializers.CharField(source='branch.name', read_only=True, default='')
    customer_name = serializers.CharField(source='user.username', read_only=True)
    vehicle_info = serializers.SerializerMethodField()
    terms_and_conditions = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = [
            'id', 'coupon_code', 'qr_token', 'code_hash', 'status',
            'deal', 'deal_title', 'merchant', 'merchant_name', 'branch', 'branch_name',
            'user', 'customer_name', 'vehicle', 'vehicle_info',
            'valid_from', 'valid_until', 'issued_at', 'redeemed_at', 'purchase_datetime',
            'is_valid', 'qr_code_image', 'terms_and_conditions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['coupon_code', 'code_hash', 'qr_token', 'created_at', 'updated_at']

    def get_is_valid(self, obj):
        return obj.is_valid()

    def get_vehicle_info(self, obj):
        if obj.vehicle:
            return str(obj.vehicle)
        return None

    def get_qr_code_image(self, obj):
        # Generate base64 QR code for mobile offline display
        if not HAS_QRCODE:
            return None
        try:
            qr = qrcode.QRCode(box_size=4, border=2)
            qr_data = obj.qr_token or obj.coupon_code
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{image_base64}"
        except Exception:
            return None

    def get_terms_and_conditions(self, obj):
        if obj.deal and hasattr(obj.deal, 'terms_and_conditions'):
            terms = obj.deal.terms_and_conditions
            if isinstance(terms, str):
                return [t.strip() for t in terms.split('\n') if t.strip()]
            elif isinstance(terms, list):
                return terms
        return []

class PromoCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = PromoCode
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'min_purchase', 'max_discount', 'start_date', 'end_date',
            'is_active', 'usage_limit', 'times_used', 'is_valid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['times_used', 'created_at', 'updated_at']

    def get_is_valid(self, obj):
        return obj.is_valid()

class RedemptionSerializer(serializers.ModelSerializer):
    coupon_code = serializers.CharField(source='coupon.coupon_code', read_only=True)
    deal_title = serializers.CharField(source='coupon.deal.title', read_only=True)
    customer_name = serializers.CharField(source='coupon.user.username', read_only=True)
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True, default='')
    staff_name = serializers.CharField(source='staff_user.username', read_only=True, default='')

    class Meta:
        model = Redemption
        fields = [
            'id', 'coupon', 'coupon_code', 'deal_title', 'customer_name',
            'merchant', 'merchant_name', 'branch', 'branch_name',
            'staff_user', 'staff_name', 'device_fingerprint',
            'redeemed_at', 'method', 'receipt_number', 'status', 'notes',
            'reversal_reason'
        ]
        read_only_fields = ['receipt_number', 'redeemed_at']

class WorkOrderSerializer(serializers.ModelSerializer):
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True, default='')
    vehicle_info = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source='customer.username', read_only=True, default='')
    technician_name = serializers.CharField(source='technician.username', read_only=True, default='')

    class Meta:
        model = WorkOrder
        fields = [
            'id', 'work_order_number', 'coupon', 'redemption',
            'merchant', 'merchant_name', 'branch', 'branch_name',
            'vehicle', 'vehicle_info', 'customer', 'customer_name',
            'technician', 'technician_name', 'status',
            'arrival_mileage_km', 'completion_note',
            'started_at', 'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['work_order_number', 'created_at', 'updated_at']

    def get_vehicle_info(self, obj):
        if obj.vehicle:
            return str(obj.vehicle)
        return None

class CouponEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponEvent
        fields = '__all__'
 