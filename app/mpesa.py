import requests
import datetime
from datetime import datetime
from requests.auth import HTTPBasicAuth
import base64
import json


def get_mpesa_token():
  consumer_key = "PCAA3puNkcLCwoswYVFHyxrYxt5c7F0Z"
  consumer_secret = "XABzYo0UseLUdUwA"
  api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

  # make a get request using python requests liblary
  r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

  # return access_token from response
  print(r.text.encode('utf8'))
  return r.json()['access_token']



def send_money_request(amount,phone_number):
  access_token = get_mpesa_token()

  passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

  headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
  }
  now = datetime.now()
  now_string = now.strftime("%Y%m%d%H%M%S")
  print(now_string)
  encode_data = "174379"+passkey+now_string

  # encode business_shortcode, online_passkey and current_time (yyyyMMhhmmss) to base64
  passkey  = base64.b64encode(encode_data.encode('utf-8'))

  payload = {
    "BusinessShortCode": "174379",
    "Password": f"{passkey.decode('utf-8')}",
    "Timestamp": f"{now_string}",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": f"{phone_number}",
    "PartyB": "174379",
    "PhoneNumber": f"{phone_number}",
    "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
    "AccountReference": "MIFSTBANK",
    "TransactionDesc": "Money Deposit"}



  response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = json.dumps(payload))
  print(response.text.encode('utf8'))