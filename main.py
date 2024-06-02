# main.py
from cassandra.cqlengine.management import sync_table

from src.database import DatabaseManager
from src.nasdaq_api_client import fetch_financial_data
from src.data_processor import transform_data, store_financial_data
from src.models import initialize_cassandra_connection, create_financial_data_model
from init_scripts.sp500_symbols import sp500_symbols
from init_scripts.populate_sp500_data import get_or_create_source_id, get_or_create_asset_id


def main():
    db = DatabaseManager()
    try:
        db.create_keyspace()
        db.create_tables()

        # Initialize Cassandra connection
        initialize_cassandra_connection()

        # Get or create the data source
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

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
