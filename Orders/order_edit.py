import requests
import json
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Constants for authentication (pulled securely from .env)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
base_url = 'https://fapi.niyam.exchange'

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

# Function to edit/update order
def edit_order(client_order_id, quantity=None, stop_price=None, price=None):
    # Generate the current timestamp
    timestamp = str(int(time.time() * 1000))

    # Prepare the request body (JSON)
    params = {
        'clientOrderId': str(client_order_id),
        'timestamp': timestamp
    }
    if(quantity):
        params['quantity'] = int(quantity)
    if(stop_price):
        params['stopPrice'] = int(stop_price)
    if(price):
        params['price'] = int(price)

    # Convert the request body to a JSON string for signing
    data_to_sign = json.dumps(params, separators=(',', ':'))

    # Generate the signature
    signature = generate_signature(api_secret, data_to_sign)

    # Headers for the PATCH request
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature
    }

    # Construct the full URL
    edit_order_url = f"{base_url}/v1/order/edit-order"

    try:
        # Send the PATCH request to edit the order
        response = requests.patch(edit_order_url, json=params, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('Order edit request sent', json.dumps(response_data, indent=4), "for:", quantity)
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response is not None else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example usage: Replace 'YOUR_CLIENT_ORDER_ID' with the actual ID
    edit_order("11", quantity=1)