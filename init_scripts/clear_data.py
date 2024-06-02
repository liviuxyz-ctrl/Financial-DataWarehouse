# init_scripts/clear_data.py
import os
from src.models import create_financial_data_model, Asset, DataSource
from cassandra.cqlengine.management import drop_table
from src.models import initialize_cassandra_connection
from init_scripts.sp500_symbols import sp500_symbols


def clear_tables():
    # Enable schema management
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    initialize_cassandra_connection()

    for symbol in sp500_symbols:
        model = create_financial_data_model(symbol)
        drop_table(model)
        print(f"Table for {symbol} has been cleared.")


if __name__ == "__main__":
    clear_tables()
