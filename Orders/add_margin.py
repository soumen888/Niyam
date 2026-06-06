import requests
import hmac
import hashlib
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Constants for authentication (pulled securely from .env)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def add_margin():
    position_id = input("Enter the positionId: ")
    amount_input = input("Enter the amount: ")

    add_margin_url = "https://api.niyam.exchange/v1/order/add-margin"

    try:
        amount = int(amount_input)
    except ValueError:
        amount = float(amount_input)

    timestamp = str(int(time.time() * 1000))

    params = {
        'positionId': position_id,
        'amount': amount,
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
    add_margin()