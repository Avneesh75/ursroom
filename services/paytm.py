import requests
import json

from services.constant import PAYTM_MERCHANT_ID, PAYTM_MERCHANT_KEY, PAYTM_WEBSITE, PAYTM_CALLBACK_URL

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import paytmchecksum

def paytm_initiate_payment(order_id, amount, user_email, HOST_NAME):
    paytmParams = dict()
    paytmParams["body"] = {
        "requestType" : "Payment",
        "mid" : PAYTM_MERCHANT_ID,
        "websiteName" : PAYTM_WEBSITE,
        "orderId" : order_id,
        "callbackUrl" : f"{HOST_NAME}{PAYTM_CALLBACK_URL}",
        "txnAmount" : {
            "value" : amount,
            "currency" : "INR",
        },
        "userInfo" : {
            "custId" : user_email,
        },
    }
    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)
    paytmParams["head"] = {
        "signature" : checksum
    }
    post_data = json.dumps(paytmParams)
    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MERCHANT_ID}&orderId={order_id}"
    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return response["body"]["txnToken"]

def paytm_verify_payment(order_id):
    paytmParams = dict()
    paytmParams["body"] = {
        "mid" : PAYTM_MERCHANT_ID,
        "orderId" : order_id,
    }
    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

    paytmParams["head"] = {
        "signature"	: checksum
    }
    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/v3/order/status"

    # for Production
    # url = "https://securegw.paytm.in/v3/order/status"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    return response["body"]

