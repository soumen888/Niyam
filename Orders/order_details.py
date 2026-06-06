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

def order_details():
    # Function to fetch order details based on client order id
    client_order_id = input("Enter the client order Id: ")
    timestamp = str(int(time.time() * 1000))
    order_url = "https://api.niyam.exchange/v1/order"
    url = f"{order_url}/{client_order_id}"
    
    params = {
        'timestamp': timestamp
    }
    
    query_string = f"timestamp={params['timestamp']}"
    signature = generate_signature(api_secret, query_string)
    
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }
    
    try:
        # Send GET request to fetch order details
        response = requests.get(f"{url}?{query_string}", headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print('Order details fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    order_details()