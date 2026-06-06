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
base_url = "https://fapi.niyam.exchange"

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def get_futures_wallet_details():
    endpoint = "/v1/wallet/futures-wallet/details"
    
    # Generate the current timestamp
    timestamp = str(int(time.time() * 1000))
    
    # Optional parameters with timestamp
    params = {
        'marginAsset': 'INR',
        'timestamp': timestamp
    }
    
    # Convert params to query string
    query_string = f"marginAsset={params['marginAsset']}&timestamp={params['timestamp']}"
    
    # Generate signature
    signature = generate_signature(api_secret, query_string)
    
    # Headers for the request
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }
    
    # Construct the full URL
    wallet_details_url = f"{base_url}{endpoint}?{query_string}"
    
    try:
        # Send the GET request to fetch the futures wallet details
        response = requests.get(wallet_details_url, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('Futures wallet details:', json.dumps(response_data, indent=4))
        return response_data
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None

if __name__ == "__main__":
    get_futures_wallet_details()