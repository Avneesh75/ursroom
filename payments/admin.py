from django.contrib import admin

from payments.models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'paid']
    list_display_links = ['id', 'user']
    search_fields = list_display
    list_filter = ['paid']
    fieldsets = (
        (
            None, 
            {
                "fields": ["user", "amount", "paid"],
            }
        ),
        (
            "Payment Details",
            {
                "fields": ["transaction_id", "bank_transaction_id", "gateway_name", "bank_name", "payment_mode"]
            }
        ),
        (
            "Plan Details",
            {
                "fields": ["subscription_plan"]
            }
        ),
        (
            "Important Dates",
            {
                "fields": ["created_at", "updated_at"]
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")