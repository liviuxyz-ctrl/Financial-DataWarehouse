import os
import argparse
from src.data.database import DatabaseManager
from src.ingestion.load import store_financial_data, store_commodity_data
from src.data.models import initialize_cassandra_connection, create_financial_data_model, create_commodity_data_model
from init_scripts.populate_sp500_data import get_or_create_source_id, get_or_create_asset_id, populate_sp500_data


def main(limit_sp500):
    # Set environment variable for schema management
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    db = DatabaseManager()
    try:
        db.create_keyspace()
        db.create_tables()

        # Initialize Cassandra connection
        initialize_cassandra_connection()

        # Populate SP500 data with specified limit
        populate_sp500_data(limit=limit_sp500)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load SP500 financial data into the database.")
    parser.add_argument('--sp500', type=int, default=500, help='Number of S&P 500 entries to populate.')
    args = parser.parse_args()

    main(limit_sp500=args.sp500)
