import requests
import json

base_url = 'https://api.niyam.exchange'

def get_exchange_info():
    full_url = f"{base_url}/v1/exchange/exchangeInfo"
    
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        
        response_data = response.json()
        print('Exchange information fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    get_exchange_info()