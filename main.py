# main.py
from src.database import DatabaseManager
from src.nasdaq_api_client import fetch_financial_data
from src.data_processor import transform_data, store_financial_data
from src.models import initialize_cassandra_connection, Asset, DataSource
import uuid


def main():
    try:
        db = DatabaseManager()
        db.create_keyspace()
        db.create_tables()

        initialize_cassandra_connection()

        # Add or retrieve Asset and DataSource entries
        asset = Asset.create(asset_id=uuid.uuid4(), name='Apple Inc.', type='Stock')
        source = DataSource.create(source_id=uuid.uuid4(), source_name='Nasdaq Data Link')

        symbol = 'AAPL'  # Example symbol for Apple Inc.
        raw_data = fetch_financial_data(symbol)
        print("Raw data fetched:", raw_data)

        transformed_data = transform_data(symbol, raw_data)
        store_financial_data(asset.asset_id, source.source_id, transformed_data)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if db:
            db.close()


if __name__ == "__main__":
    main()
