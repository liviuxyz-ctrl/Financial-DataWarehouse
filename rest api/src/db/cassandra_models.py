from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.connection import setup
import uuid

class Asset(Model):
    __keyspace__ = 'financial_data'
    asset_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    type = columns.Text()

class DataSource(Model):
    __keyspace__ = 'financial_data'
    source_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    source_name = columns.Text(index=True)

class BaseFinancialData(Model):
    __abstract__ = True
    asset_id = columns.UUID(partition_key=True)
    source_id = columns.UUID(partition_key=True)
    business_date = columns.Date(primary_key=True)
    system_time = columns.DateTime(primary_key=True, clustering_order="DESC")
    symbol = columns.Text(index=True)
    open = columns.Float()
    high = columns.Float()
    low = columns.Float()
    close = columns.Float()
    volume = columns.BigInt()

class BaseCommodityData(Model):
    __abstract__ = True
    asset_id = columns.UUID(partition_key=True)
    source_id = columns.UUID(partition_key=True)
    business_date = columns.Date(primary_key=True)
    system_time = columns.DateTime(primary_key=True, clustering_order="DESC")
    symbol = columns.Text(index=True)
    value = columns.Float()

def initialize_cassandra_connection():
    setup(["127.0.0.1"], "financial_data", protocol_version=4)

def create_financial_data_model(symbol):
    class_name = f'FinancialData_{symbol.lower()}'
    attrs = dict(
        __module__=__name__,
        __keyspace__='financial_data',
        asset_id=columns.UUID(partition_key=True),
        source_id=columns.UUID(partition_key=True),
        business_date=columns.Date(primary_key=True),
        system_time=columns.DateTime(primary_key=True, clustering_order="DESC"),
        symbol=columns.Text(index=True),
        open=columns.Float(),
        high=columns.Float(),
        low=columns.Float(),
        close=columns.Float(),
        volume=columns.BigInt(),
    )
    return type(class_name, (BaseFinancialData,), attrs)

def create_commodity_data_model(symbol):
    class_name = f"CommodityData_{symbol.lower()}"
    attrs = {
        '__module__': __name__,
        '__keyspace__': 'commodities_data',
        'asset_id': columns.UUID(partition_key=True),
        'source_id': columns.UUID(partition_key=True),
        'business_date': columns.Date(primary_key=True),
        'system_time': columns.DateTime(primary_key=True, clustering_order="DESC"),
        'symbol': columns.Text(index=True),
        'value': columns.Float()
    }
    return type(class_name, (BaseCommodityData,), attrs)
