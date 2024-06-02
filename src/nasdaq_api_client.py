# src/nasdaq_api_client.py
import requests
from src.config import API_KEY  # Ensure API key is securely imported from config


def fetch_financial_data(symbol):
    url = f"https://data.nasdaq.com/api/v3/datasets/WIKI/{symbol}.json?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['dataset']['data']
    else:
        try:
            error_info = response.json()
            if 'quandl_error' in error_info:
                error_message = error_info['quandl_error']['message']
                raise Exception(f"Error from API: {error_message}")
            else:
                raise Exception("Error: Dataset not found or URL is incorrect.")
        except requests.JSONDecodeError:
            raise Exception(f"Error: Response not in JSON format. Status Code: {response.status_code}")
