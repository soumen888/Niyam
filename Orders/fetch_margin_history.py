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
base_url = 'https://api.niyam.exchange'

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def fetch_margin_history():
    endpoint = "/v1/order/fetch-margin-history"
    symbol = input("Enter the symbol (e.g., BTC): ").upper()
    
    pageSize = 100
    sortOrder = "desc"
    
    # Generate current timestamp for signing
    timestamp = str(int(time.time() * 1000))
    
    # Prepare query parameters
    params = {
        'pageSize': str(pageSize),
        'sortOrder': sortOrder,
        'symbol': symbol,
        'timestamp': timestamp
    }
    
    # Convert params to query string
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    
    # Generate signature
    signature = generate_signature(api_secret, query_string)
    
    # Headers for the request
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }
    
    full_url = f"{base_url}{endpoint}?{query_string}"
    
    try:
        # Send the GET request to fetch margin history
        response = requests.get(full_url, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('Margin history fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response is not None else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    fetch_margin_history()