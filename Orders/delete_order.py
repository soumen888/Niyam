import time
import json
import requests
import hmac
import hashlib
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Constants for authentication (pulled securely from .env)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def delete_order():
    client_order_id = input("Enter the clientOrderId to delete: ")
    delete_order_url = "https://api.niyam.exchange/v1/order/delete-order"
    timestamp = str(int(time.time() * 1000))
    
    params = {
        'clientOrderId': client_order_id,
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
        response = requests.delete(delete_order_url, json=params, headers=headers)
        response.raise_for_status()
        print(f"Order with clientOrderId {client_order_id} deleted successfully.")
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    delete_order()