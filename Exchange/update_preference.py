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
base_url = "https://api.niyam.exchange"

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def update_preference():
    endpoint = "/v1/exchange/update/preference"
    leverage = 10 # Ensure leverage is an integer
    contract_name = "BTCINR" # Replace with the appropriate contract name
    margin_mode = "ISOLATED" # Ensure marginMode is either 'ISOLATED' or 'CROSS'

    # Generate the current timestamp
    timestamp = str(int(time.time() * 1000))

    # Prepare the request body (JSON)
    params = {
        'leverage': leverage,
        'marginMode': margin_mode,
        'contractName': contract_name,
        'timestamp': timestamp
    }

    # Convert the request body to a JSON string for signing
    data_to_sign = json.dumps(params, separators=(',', ':'))

    # Generate the signature (ensure 'generate_signature' is properly defined)
    signature = generate_signature(api_secret, data_to_sign)

    # Headers for the POST request
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature
    }

    # Construct the full URL
    update_preference_url = f"{base_url}{endpoint}"

    try:
        # Send the POST request to update the preference
        response = requests.post(update_preference_url, json=params, headers=headers)
        response.raise_for_status() # Raises an error for 4xx/5xx responses
        response_data = response.json()
        print('Preference updated successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response is not None else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    update_preference()