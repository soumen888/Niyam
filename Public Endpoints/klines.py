import requests
import json

base_url = 'https://api.niyam.exchange'

def get_kline_data():
    try:
        pair = input("Enter the trading pair (e.g., BTCINR): ").strip().upper()
        pair = pair.replace('-', '').replace('_', '').replace('/', '')
        
        if pair and not pair.endswith('INR') and not pair.endswith('USDT'):
            pair += 'INR'
            
        interval = input("Enter the interval (e.g., 1m, 5m, 1h): ").lower()
        
        params = {
            'pair': pair,
            'interval': interval,
            'limit': 1000
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        kline_url = f"{base_url}/v1/market/klines?priceType=MARK_PRICE"
        
        response = requests.post(kline_url, json=params, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        print('Kline data fetched successfully:', json.dumps(response_data, indent=4))
        
    except ValueError:
        print("Please enter valid inputs for pair, interval.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    get_kline_data()