import time
import json
import requests
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
base_url = 'https://api.niyam.exchange'

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def close_all_positions():
    endpoint = "/v1/positions/close-all-positions"
    
    timestamp = str(int(time.time() * 1000))
    
    params = {
        'timestamp': timestamp
    }
    
    data_to_sign = json.dumps(params, separators=(',', ':'))
    
    signature = generate_signature(api_secret, data_to_sign)
    
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature
    }
    
    cancel_orders_url = f"{base_url}{endpoint}"
    
    try:
        # Send the DELETE request to cancel all orders
        response = requests.delete(cancel_orders_url, json=params, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('All orders canceled successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    close_all_positions()