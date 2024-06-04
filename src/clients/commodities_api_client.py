# src/clients/commodities_api_client.py
import requests
from src.config.settings import Config


def fetch_commodity_data(symbol):
    function = symbol
    interval = "monthly"
    url = f"https://www.alphavantage.co/query?function={function}&interval={interval}&apikey={Config.ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Raw response for {symbol}: {response.json()}")  # Debugging line
        return response.json()
    else:
        response.raise_for_status()
