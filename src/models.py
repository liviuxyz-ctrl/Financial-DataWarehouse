from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
import uuid
import datetime


class Asset(Model):
    __keyspace__ = 'financial_data'
    asset_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(index=True)
    type = columns.Text()


class DataSource(Model):
    __keyspace__ = 'financial_data'
    source_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    source_name = columns.Text(index=True)


class BaseFinancialData(Model):
    __abstract__ = True  # This model will be used as a base class for dynamic tables
    asset_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    source_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    business_date = columns.Date(primary_key=True)
    system_time = columns.DateTime(primary_key=True, clustering_order="DESC")
    open = columns.Float()
    high = columns.Float()
    low = columns.Float()
    close = columns.Float()
    volume = columns.BigInt()
    symbol = columns.Text()


def create_keyspace_simple(session, keyspace_name, replication_factor):
    query = f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace_name}
    WITH REPLICATION = {{
        'class': 'SimpleStrategy',
        'replication_factor': {replication_factor}
    }};
    """
    session.execute(query)


def create_financial_data_model(symbol):
    class_name = f"FinancialData_{symbol.lower()}"
    attrs = {
        '__module__': __name__,
        '__keyspace__': 'financial_data',
        'asset_id': columns.UUID(partition_key=True),
        'source_id': columns.UUID(partition_key=True),
        'business_date': columns.Date(primary_key=True),
        'system_time': columns.DateTime(primary_key=True, clustering_order="DESC"),
        'open': columns.Float(),
        'high': columns.Float(),
        'low': columns.Float(),
        'close': columns.Float(),
        'volume': columns.BigInt(),
        'symbol': columns.Text()
    }
    return type(class_name, (BaseFinancialData,), attrs)


def initialize_cassandra_connection():
    # Initialize the connection to the Cassandra cluster with protocol version 4
    cluster = Cluster(['localhost'], protocol_version=4)
    session = cluster.connect()
    create_keyspace_simple(session, 'financial_data', 3)  # Assuming a replication factor of 3
    connection.setup(['localhost'], "financial_data", protocol_version=4)
    sync_table(Asset)
    sync_table(DataSource)
