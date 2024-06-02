import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.query import BatchQuery
from src.models import create_financial_data_model


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


def store_financial_data(asset_id, source_id, transformed_data):
    symbol = transformed_data[0]['symbol'].lower()  # Assuming all data points have the same symbol
    FinancialDataModel = create_financial_data_model(symbol)
    sync_table(FinancialDataModel)

    with BatchQuery() as b:
        for data_point in transformed_data:
            FinancialDataModel.batch(b).create(
                asset_id=asset_id,
                source_id=source_id,
                business_date=data_point['date'],
                system_time=datetime.datetime.now(),
                open=data_point['open'],
                high=data_point['high'],
                low=data_point['low'],
                close=data_point['close'],
                volume=data_point['volume'],
                symbol=data_point['symbol']
            )
