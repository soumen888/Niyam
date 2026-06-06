import time
import json
import requests
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Constants for authentication (pulled securely from .env)
api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

# Function to fetch trade history
def trade_history():
    # Generate the current timestamp
    timestamp = str(int(time.time() * 1000))
    trade_history_url = "https://api.niyam.exchange/v1/user-data/trade-history"

    # Prepare parameters with the current timestamp
    params = {
        'sortOrder': 'desc',
        'pageSize': 100,
        'timestamp': timestamp
    }

    # Generate the query string
    query_string = f"sortOrder={params['sortOrder']}&pageSize={params['pageSize']}&timestamp={params['timestamp']}"

    # Generate the signature using the current timestamp
    signature = generate_signature(api_secret, query_string)

    # Prepare headers
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }

    try:
        # Send GET request to fetch trade history with the timestamp parameter
        response = requests.get(f"{trade_history_url}?{query_string}", headers=headers)
        response.raise_for_status() # Raises an error for bad HTTP responses
        response_data = response.json()
        print('Trade history fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    trade_history()