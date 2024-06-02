import requests
from .config import API_KEY  # Assume API key is stored in config.py


def fetch_financial_data(symbol):
    url = f"https://data.nasdaq.com/api/v3/datasets/WIKI/{symbol}.json?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['dataset']['data']
    else:
        response.raise_for_status()
