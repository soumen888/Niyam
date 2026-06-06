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
base_url = 'https://api.niyam.exchange'

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def place_order():
    # Generate the current timestamp in milliseconds
    timestamp = str(int(time.time() * 1000))

    # Define the order parameters
    params = {
        'timestamp': timestamp,              # Current timestamp in milliseconds
        'placeType': 'ORDER_FORM',          # Type of order placement, e.g., 'ORDER_FORM'
        'quantity': 0.002,                   # Quantity of the asset to trade
        'side': 'BUY',                       # Order side, either 'BUY' or 'SELL'
        'symbol': 'BTCINR',                # Trading pair, e.g., Bitcoin to USDT
        'type': 'MARKET',                   # Order type, either 'MARKET' or 'LIMIT'
        'reduceOnly': False,                # Whether to reduce an existing position only
        'marginAsset': 'INR',               # The asset used as margin (INR in this case)
        'deviceType': 'WEB',                # Device type (e.g., WEB, MOBILE)
        'userCategory': 'EXTERNAL',         # User category (e.g., EXTERNAL, INTERNAL)
        'price': 5000000,                     # Price for the limit order (included here but irrelevant for market orders)
    }

    # Convert the parameters to a JSON string to sign
    data_to_sign = json.dumps(params, separators=(',', ':'))

    # Generate the signature for authentication
    signature = generate_signature(api_secret, data_to_sign)

    # Define the headers including the API key and the signature
    headers = {
        'api-key': api_key,
        'signature': signature,
    }

    try:
        # Send the POST request to place the order
        response = requests.post(f'{base_url}/v1/order/place-order', json=params, headers=headers)

        # Raise an HTTPError if the response status is 4xx or 5xx
        response.raise_for_status()

        # Parse the JSON response data
        response_data = response.json()

        # Print the success message with the order details
        print('Order placed successfully:', json.dumps(response_data, indent=4))

    except requests.exceptions.HTTPError as err:
        # Handle HTTP errors specifically
        print(f"Error: {err.response.text if err.response is not None else err}")

    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    place_order()