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
base_url = "https://api.niyam.exchange"

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def get_transaction_history():
    # Default values for optional parameters
    start_timestamp = None
    end_timestamp = None
    sort_order = 'desc'
    page_size = 100
    symbol = None
    trade_id = None
    position_id = None

    # Generate the current timestamp (used as part of the authentication/signing process)
    timestamp = str(int(time.time() * 1000))

    # Prepare query parameters with required and optional fields
    params = {
        'sortOrder': sort_order,
        'pageSize': page_size,
        'timestamp': timestamp
    }

    # Include optional parameters only if they are provided
    if start_timestamp:
        params['startTimestamp'] = start_timestamp
    if end_timestamp:
        params['endTimestamp'] = end_timestamp
    if symbol:
        params['symbol'] = symbol
    if trade_id:
        params['tradeId'] = trade_id
    if position_id:
        params['positionId'] = position_id

    # Convert the parameters to a query string to be signed
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])

    # Generate the signature (assuming generate_signature is defined)
    signature = generate_signature(api_secret, query_string)

    # Headers for the GET request
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }

    # Construct the full URL with the query string
    full_url = f"{base_url}/v1/user-data/transaction-history?{query_string}"

    try:
        # Send the GET request to fetch transaction history
        response = requests.get(full_url, headers=headers)
        response.raise_for_status() # Raises an error for HTTP 4xx/5xx responses
        response_data = response.json()
        print('Transaction history fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        # Handle specific HTTP errors
        print(f"HTTP Error: {err.response.text if err.response else 'No response text'}")
    except Exception as e:
        # Handle any other exceptions
        print(f"Failed {response.status_code}: {response.text}")

if __name__ == "__main__":
    get_transaction_history()