import requests
import json

base_url = 'https://api.niyam.exchange'

def get_24hr_ticker_update():
    contract_pair = input("Enter the contract pair (e.g., BTC, ETH): ").strip().upper()
    contract_pair = contract_pair.replace('-', '').replace('_', '').replace('/', '')
    
    if contract_pair and not contract_pair.endswith('INR') and not contract_pair.endswith('USDT'):
        contract_pair += 'INR'
        
    if not contract_pair:
        print("Invalid contract pair. Please enter a valid contract pair (e.g., BTC, ETH).")
        return
        
    full_url = f"{base_url}/v1/market/ticker24Hr/{contract_pair}"
    
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        
        response_data = response.json()
        print('24-hour ticker update fetched successfully:', json.dumps(response_data, indent=4))
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    get_24hr_ticker_update()