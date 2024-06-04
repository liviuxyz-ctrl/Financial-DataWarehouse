# tests/base_test.py
import unittest
import os
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine import connection
from src.data.models import Asset, DataSource, FinancialData, initialize_cassandra_connection
from src.data.database import DatabaseManager


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set the environment variable for schema management
        os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

        # Initialize the database manager and create keyspace and tables
        cls.db = DatabaseManager()
        cls.db.create_keyspace()
        cls.db.create_tables()

        # Initialize Cassandra connection
        initialize_cassandra_connection()

    @classmethod
    def tearDownClass(cls):
        # Drop the tables and close the database connection
        drop_table(Asset)
        drop_table(DataSource)
        drop_table(FinancialData)
        cls.db.close()
