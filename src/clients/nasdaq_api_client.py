# src/clients/nasdaq_api_client.py
import requests
from src.config.settings import Config


def fetch_financial_data(symbol):
    try:
        url = f"https://data.nasdaq.com/api/v3/datasets/WIKI/{symbol}.json?api_key={Config.API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['dataset']['data']
        else:
            response.raise_for_status()
    except Exception as e:
        print(e)
