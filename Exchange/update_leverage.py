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

def update_leverage():
    # User inputs
    leverage = int(input("Enter the leverage value: "))
    contract_name_input = input("Enter the contract name: ").strip().upper().replace("/", "").replace("-", "")
    contract_name = contract_name_input if contract_name_input.endswith("INR") else contract_name_input + "INR"
    
    timestamp = str(int(time.time() * 1000))
    
    params = {
        'leverage': int(leverage),
        'contractName': contract_name,
        'timestamp': timestamp
    }
    
    data_to_sign = json.dumps(params, separators=(',', ':'))
    
    signature = generate_signature(api_secret, data_to_sign)
    
    headers = {
        'api-key': api_key,
        'Content-Type': 'application/json',
        'signature': signature
    }
    
    update_leverage_url = f"{base_url}/v1/exchange/update/leverage"
    
    try:
        response = requests.post(update_leverage_url, json=params, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        print('Leverage updated successfully:', json.dumps(response_data, indent=4))
        
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response is not None else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    update_leverage()