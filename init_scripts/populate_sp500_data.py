# init_scripts/populate_sp500_data.py
import time
from cassandra.cqlengine import connection
from src.database import DatabaseManager
from src.models import create_financial_data_model, DataSource, Asset, initialize_cassandra_connection
from src.nasdaq_api_client import fetch_financial_data
from src.data_processor import transform_data, store_financial_data
from init_scripts.sp500_symbols import sp500_symbols  # Ensure sp500_symbols.py contains the list of S&P 500 symbols
from cassandra.cqlengine.management import sync_table


def get_or_create_source_id(source_name):
    # Check if the data source already exists
    existing_source = DataSource.objects(source_name=source_name).first()
    if existing_source:
        return existing_source.source_id
    # If not, create a new data source entry
    new_source = DataSource.create(source_name=source_name)
    return new_source.source_id


def get_or_create_asset_id(asset_name):
    # Check if the asset already exists
    existing_asset = Asset.objects(name=asset_name).first()
    if existing_asset:
        return existing_asset.asset_id
    # If not, create a new asset entry
    new_asset = Asset.create(name=asset_name, type='stock')
    return new_asset.asset_id


def main():
    db = DatabaseManager()
    try:
        db.create_keyspace()
        db.create_tables()
        db.session.set_keyspace('financial_data')

        initialize_cassandra_connection()

        source_id = get_or_create_source_id('Nasdaq Data Link')

        for symbol in sp500_symbols:
            asset_id = get_or_create_asset_id(symbol)
            # Dynamically create and sync the table for each symbol
            FinancialDataModel = create_financial_data_model(symbol)
            sync_table(FinancialDataModel)

            # Fetch and store financial data
            raw_data = fetch_financial_data(symbol)
            transformed_data = transform_data(symbol, raw_data)
            store_financial_data(asset_id, source_id, transformed_data)

            # Adding a delay to avoid being banned by the API
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
