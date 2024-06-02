from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
import uuid
import datetime


class Asset(Model):
    __keyspace__ = 'financial_data'
    asset_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text()
    type = columns.Text()


class DataSource(Model):
    __keyspace__ = 'financial_data'
    source_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    source_name = columns.Text()


class FinancialData(Model):
    __keyspace__ = 'financial_data'
    asset_id = columns.UUID(partition_key=True)
    source_id = columns.UUID(partition_key=True)
    business_date = columns.Date(primary_key=True)
    system_time = columns.DateTime(primary_key=True, clustering_order="DESC")
    open = columns.Float()
    high = columns.Float()
    low = columns.Float()
    close = columns.Float()
    volume = columns.BigInt()


def initialize_cassandra_connection():
    # Initialize the connection to the Cassandra cluster with protocol version 4
    connection.setup(['localhost'], "cqlengine", protocol_version=4)
    sync_table(Asset)
    sync_table(DataSource)
    sync_table(FinancialData)
