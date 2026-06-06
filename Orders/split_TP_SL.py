import requests
import json
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

load_dotenv()

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def split_tp_sl():
    # These should be provided as environment variables or constants
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('SECRET_KEY')

    position_id = input("Enter the positionId: ")
    tp_quantity_input = input("Enter the TP quantity: ")
    tp_price_input = input("Enter the TP price: ")
    sl_quantity_input = input("Enter the SL quantity: ")
    sl_price_input = input("Enter the SL price: ")

    add_margin_url = "https://api.niyam.exchange/v2/order/split-tp-sl"

    try:
        tp_quantity = int(tp_quantity_input)
    except ValueError:
        tp_quantity = float(tp_quantity_input)

    try:
        tp_price = int(tp_price_input)
    except ValueError:
        tp_price = float(tp_price_input)

    try:
        sl_quantity = int(sl_quantity_input)
    except ValueError:
        tp_price = float(sl_quantity_input)

    try:
        sl_price = int(sl_price_input)
    except ValueError:
        sl_price = float(sl_price_input)

    timestamp = str(int(time.time() * 1000))

    params = {
        'positionId': position_id,
        'splitTakeProfitOrders': [{
            'quantity': tp_quantity,
            'price': tp_price
        }],
        'splitStopLossOrders': [{
            'quantity': sl_quantity,
            'price': sl_price
        }],
        'timestamp': timestamp
    }

    data_to_sign = json.dumps(params, separators=(',', ':'))
    signature = generate_signature(api_secret, data_to_sign)

    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature,
    }

    try:
        response = requests.post(add_margin_url, json=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print('Margin added successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    split_tp_sl()