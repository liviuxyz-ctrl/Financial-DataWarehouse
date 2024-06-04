# init_scripts/populate_sp500_data.py
import time
from cassandra.cqlengine.management import sync_table
from src.clients.nasdaq_api_client import fetch_financial_data
from src.data.models import initialize_cassandra_connection, create_financial_data_model, DataSource, Asset
from src.ingestion.transform import transform_financial_data
from src.ingestion.load import store_financial_data
from src.init_scripts.sp500_symbols import sp500_symbols
import uuid


def get_or_create_source_id(source_name):
    source = DataSource.objects.filter(source_name=source_name).first()
    if source is None:
        source = DataSource.create(source_id=uuid.uuid4(), source_name=source_name)
    return source.source_id


def get_or_create_asset_id(symbol):
    asset = Asset.objects.filter(name=symbol).first()
    if asset is None:
        asset = Asset.create(asset_id=uuid.uuid4(), name=symbol, type='Stock')
    return asset.asset_id


def populate_sp500_data():
    initialize_cassandra_connection()
    source_id = get_or_create_source_id('Nasdaq Data Link')

    for symbol in sp500_symbols:
        asset_id = get_or_create_asset_id(symbol)
        FinancialDataModel = create_financial_data_model(symbol)
        sync_table(FinancialDataModel)
        raw_data = fetch_financial_data(symbol)
        transformed_data = transform_financial_data(symbol, raw_data)
        store_financial_data(asset_id, source_id, transformed_data)
        time.sleep(1)  # To avoid hitting the rate limit


if __name__ == "__main__":
    populate_sp500_data()
