import json
import razorpay
from django.http.response import Http404

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import mail_managers, send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from razorpay import client

from .models import Payment
from account.models import Subscription
from services.constant import PAYTM_MERCHANT_ID
from services.paytm import paytm_initiate_payment, paytm_verify_payment

User = get_user_model()

# RAZORPAY_KEY_ID = "rzp_test_uZIppd9mUOdPuG"
# RAZORPAY_KEY_SECRET = "UHJ7kpB6CllmveHGN1lv8yPb"

# client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


# @login_required
# def billing(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         amount = int(data.get("amount"))
#         payment = client.order.create({"amount":amount*100, "currency":"INR"})
#         subs = Subscription.objects.get(id=int(data.get("subscription")))
#         order = Payment(user=request.user, amount=amount, order_id=payment['id'], subscription_plan=subs)
#         order.save()
#         return JsonResponse({"data": payment})
#     else:
#         raise Http404()


# @login_required
# @csrf_exempt
# def success_payment(request):
#     if request.method == "POST":
#         data = request.POST
#         print(data)
#         order_id = Payment.objects.filter(user=request.user).last().order_id
#         parameters = {
#             "razorpay_order_id": order_id,
#             "razorpay_payment_id": data['razorpay_payment_id'],
#             "razorpay_signature": data['razorpay_signature']
#         }
#         signature = client.utility.verify_payment_signature(parameters=parameters)
#         print(signature)
        
#         if signature is not None:
#             order = Payment.objects.filter(user=request.user, order_id=data['razorpay_order_id'])
#             order.update(payment_id=data['razorpay_payment_id'], payment_signature=data['razorpay_signature'], paid=True)
#             user = User.objects.get(id=request.user.id)
#             user.subscription = order[0].subscription_plan
#             user.is_subscribed = True
#             user.save()
#             messages.success(request, "Your payment was successfull.")
#             return redirect("ursroom_room_user_profile")
#         messages.error(request, "Your payment was not successfull.")
#         return redirect("ursroom_room_user_profile")
#     else:
#         raise Http404()


@login_required
def initiate_payment(request):
    if request.method == 'POST':
        data = request.POST
        amount = float(data.get("amount"))
        subs = Subscription.objects.get(id=int(data.get("subscription")))
        order = Payment(user=request.user, amount=amount, subscription_plan=subs)
        order.save()
        host = request.META['HTTP_HOST']
        url_scheme = request.META['wsgi.url_scheme']
        HOST_URL = f"{url_scheme}://{host}"
        txn_token = paytm_initiate_payment(order.id, amount, request.user.email, HOST_URL)
        context = {
            "txn_token": txn_token,
            "order_id": order.id,
            "amount": amount,
            "MID": PAYTM_MERCHANT_ID
        }
        return render(request, "payment-processing.html", context)
    else:
        raise Http404()


@csrf_exempt
def handle_payment(request):
    if request.method == "POST":
        data = request.POST
        response = paytm_verify_payment(data["ORDERID"])
        if (response["resultInfo"]["resultStatus"] == "TXN_SUCCESS"):
            order = Payment.objects.get(id=response["orderId"])
            order.transaction_id = response["txnId"]
            order.bank_transaction_id = response["bankTxnId"]
            order.bank_name = response["bankName"]
            order.gateway_name = response["gatewayName"]
            order.payment_mode = response["paymentMode"]
            order.paid = True
            order.save()
            user = User.objects.get(id=order.user.id)
            user.subscription = order.subscription_plan
            user.is_subscribed = True
            user.save()
            messages.success(request, "Your payment was successfull.")
        else:
            messages.error(request, "Your payment was not successfull.")
        return redirect("ursroom_room_user_profile")
