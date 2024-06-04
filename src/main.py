# src/main.py
import datetime
from src.data.database import DatabaseManager
from src.clients.nasdaq_api_client import fetch_financial_data
from src.clients.commodities_api_client import fetch_commodity_data
from src.ingestion.transform import transform_financial_data
from src.ingestion.load import store_financial_data
from src.data.models import initialize_cassandra_connection, create_financial_data_model, create_commodity_data_model
from cassandra.cqlengine.management import sync_table
from src.init_scripts.sp500_symbols import sp500_symbols
from src.init_scripts.populate_sp500_data import get_or_create_source_id, get_or_create_asset_id


def main():
    db = DatabaseManager()
    try:
        db.create_keyspace()
        db.create_tables()

        # Initialize Cassandra connection
        initialize_cassandra_connection()

        # Get or create the data source
        source_id = get_or_create_source_id('Nasdaq Data Link')

        # Handling SP500 symbols
        for symbol in sp500_symbols:
            asset_id = get_or_create_asset_id(symbol)
            FinancialDataModel = create_financial_data_model(symbol)
            sync_table(FinancialDataModel)

            raw_data = fetch_financial_data(symbol)
            transformed_data = transform_financial_data(symbol, raw_data)
            store_financial_data(asset_id, source_id, transformed_data)

        # Handling Commodities like WTI and Brent
        commodities = ['WTI', 'BRENT']
        for commodity in commodities:
            # Create and sync the specific commodity data model for each commodity
            CommodityDataModel = create_commodity_data_model(commodity)
            sync_table(CommodityDataModel)  # Sync the commodity model table with Cassandra

            # Fetch commodity-specific data
            raw_data = fetch_commodity_data(commodity)
            for data in raw_data:
                # Using the created model to store data
                CommodityDataModel.create(
                    symbol=commodity,
                    business_date=data['date'],
                    system_time=datetime.datetime.now(),
                    value=data['value'],
                    source_id=source_id
                )

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
