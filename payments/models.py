from django.db import models

from django.contrib.auth import get_user_model

from account.models import Subscription

User = get_user_model()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    bank_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    gateway_name = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    payment_mode = models.CharField(max_length=255, null=True, blank=True)
    paid = models.BooleanField(default=False)
    subscription_plan = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"