import requests
import hmac
import hashlib
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
api_secret = os.getenv('SECRET_KEY')
base_url = 'https://api.niyam.exchange'

def generate_signature(api_secret, data_to_sign):
    return hmac.new(api_secret.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def reduce_margin():
    # Collect position ID and amount to reduce from user input
    position_id = input("Enter the positionId: ")
    amountInput = input("Enter the amount to reduce: ")

    try:
        # Convert input to integer or float as necessary
        amount = int(amountInput)
    except ValueError:
        amount = float(amountInput)

    # Generate current timestamp in milliseconds
    timestamp = str(int(time.time() * 1000))

    # Prepare the request payload (JSON)
    params = {
        'positionId': position_id,
        'amount': amount,
        'timestamp': timestamp
    }

    # Convert the payload to a JSON string for signature
    data_to_sign = json.dumps(params, separators=(',', ':'))

    # Generate the signature using a helper function
    signature = generate_signature(api_secret, data_to_sign)

    # Set the headers for the POST request
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature
    }

    # Construct the full API endpoint URL
    reduce_margin_url = f"{base_url}/v1/order/reduce-margin"

    try:
        # Send the POST request to reduce margin
        response = requests.post(reduce_margin_url, json=params, headers=headers)
        response.raise_for_status() # Raises an error for HTTP responses with 4xx/5xx status codes
        response_data = response.json()
        print('Margin reduced successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response is not None else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    reduce_margin()