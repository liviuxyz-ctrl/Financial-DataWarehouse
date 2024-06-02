# src/database.py
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from models import Asset, DataSource, FinancialData


class DatabaseManager:
    def __init__(self):
        self.cluster = Cluster(['localhost'], protocol_version=4)  # Set protocol version to V4
        self.session = self.cluster.connect()
        connection.set_session(self.session)

    def create_keyspace(self):
        query = """
        CREATE KEYSPACE IF NOT EXISTS financial_data
        WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
        """
        self.session.execute(query)

    def create_tables(self):
        sync_table(Asset)
        sync_table(DataSource)
        sync_table(FinancialData)

    def close(self):
        self.cluster.shutdown()
        self.session.shutdown()
