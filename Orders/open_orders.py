import time
import hmac
import hashlib
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Constants for authentication (pulled securely from .env)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def get_open_orders():
    base_url = 'https://fapi.niyam.exchange'

    # Generate the current timestamp
    timestamp = str(int(time.time() * 1000))

    # Prepare parameters with the current timestamp
    params = f"timestamp={timestamp}"

    # Generate the signature using the current timestamp
    signature = generate_signature(api_secret, params)

    # Prepare headers
    headers = {
        'api-key': api_key,
        'signature': signature,
    }

    open_orders_url = f"{base_url}/v1/order/open-orders"

    try:
        # Send GET request to fetch open orders with the timestamp parameter
        response = requests.get(open_orders_url, headers=headers, params={'timestamp': timestamp})
        response.raise_for_status() # Raises an error for bad HTTP responses
        response_data = response.json()
        print('Open orders fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    get_open_orders()