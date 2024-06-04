# init_scripts/populate_commodities_data.py
import uuid
from cassandra.cqlengine.management import sync_table
from src.data.models import initialize_cassandra_connection, create_commodity_data_model, DataSource, Asset
from src.clients.commodities_api_client import fetch_commodity_data
from src.ingestion.transform import transform_commodity_data
from src.ingestion.load import store_commodity_data


def get_or_create_source_id(source_name):
    source = DataSource.objects.filter(source_name=source_name).first()
    if source is None:
        source = DataSource.create(source_id=uuid.uuid4(), source_name=source_name)
    return source.source_id


def get_or_create_asset_id(symbol):
    asset = Asset.objects.filter(name=symbol).first()
    if asset is None:
        asset = Asset.create(asset_id=uuid.uuid4(), name=symbol, type='Commodity')
    return asset.asset_id


def populate_commodities_data():
    initialize_cassandra_connection()
    commodities = ['WTI', 'BRENT']
    source_id = get_or_create_source_id('Alpha Vantage')

    for commodity in commodities:
        CommodityDataModel = create_commodity_data_model(commodity)
        sync_table(CommodityDataModel)
        raw_data = fetch_commodity_data(commodity)
        transformed_data = transform_commodity_data(commodity, raw_data)
        asset_id = get_or_create_asset_id(commodity)
        store_commodity_data(asset_id, source_id, transformed_data)


if __name__ == "__main__":
    populate_commodities_data()
