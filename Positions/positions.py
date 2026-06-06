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

def fetch_positions():
    position_status = input("Enter position status (open, closed, liquidated): ").upper()
    symbol = input("Enter the trading pair (e.g., BTCINR): ").upper()

    if position_status not in ["OPEN", "CLOSED", "LIQUIDATED"]:
        print("Invalid position status. Please enter 'open', 'closed', or 'liquidated'.")
        return

    # Optional parameters
    sort_order = "desc" # Default sort order
    page_size = 100 # Default page size

    # Prepare the query parameters
    params = {
        'sortOrder': sort_order,
        'pageSize': str(page_size),
        'symbol': symbol,
    }

    # Generate current timestamp
    timestamp = str(int(time.time() * 1000))
    params['timestamp'] = timestamp

    # Generate signature based on the parameters
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = generate_signature(api_secret, query_string)

    # Headers for the GET request
    headers = {
        'api-key': api_key,
        'signature': signature,
        'accept': '*/*'
    }

    # Construct the full URL including the path parameter for position status
    full_url = f"{base_url}/v1/positions/{position_status}?{query_string}"

    try:
        # Send the GET request to fetch positions
        response = requests.get(full_url, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('Positions fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    fetch_positions()