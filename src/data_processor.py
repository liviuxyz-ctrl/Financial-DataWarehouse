# src/data_processor.py
from src.models import FinancialData
import datetime


def transform_data(symbol, raw_data):
    transformed = []
    for data in raw_data:
        try:
            transformed.append({
                'symbol': symbol,
                'date': data[0],
                'open': data[1],
                'high': data[2],
                'low': data[3],
                'close': data[4],
                'volume': data[5]
            })
        except IndexError:
            print("Data format error with:", data)
    return transformed


def store_financial_data(asset_id, source_id, data):
    for data_point in data:
        FinancialData.create(
            asset_id=asset_id,
            source_id=source_id,
            business_date=data_point['date'],
            system_time=datetime.datetime.now(),  # Assuming current time as system time
            open=data_point['open'],
            high=data_point['high'],
            low=data_point['low'],
            close=data_point['close'],
            volume=data_point['volume']
        )
