# payments/admin.py

from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "status",
        "payment_method",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "currency", "payment_method", "created_at")
    search_fields = (
        "user__username",
        "transaction_id",
        "amount",
    )
    readonly_fields = (
        "id",
        "user",
        "amount",
        "currency",
        "status",
        "payment_method",
        "transaction_id",
        "payment_details",
        "error_message",
        "created_at",
        "updated_at",
        "completed_at",
    )
    autocomplete_fields = ["user"]

    def has_add_permission(self, request):
        # Transactions should generally not be added manually via admin
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent accidental deletion of payment records
        return False

