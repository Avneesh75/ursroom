from django.urls import path

from payments.views import *

urlpatterns = [
    # path("billing/", billing, name="billing"),
    # path("success-payment/", success_payment, name="success-payment"),
    path("billing", initiate_payment, name="initiate-payment"),
    path("handle-payment", handle_payment, name="handle-payment"),
]