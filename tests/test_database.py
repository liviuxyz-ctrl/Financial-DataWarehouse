# tests/test_database.py
import unittest
from cassandra.cqlengine.management import sync_table, drop_table
from cassandra.cqlengine import connection
from src.models import NasdaqData, initialize_cassandra_connection
from src.database import DatabaseManager


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseManager()
        cls.db.create_keyspace()
        cls.db.create_tables()
        initialize_cassandra_connection()

    @classmethod
    def tearDownClass(cls):
        drop_table(NasdaqData)
        cls.db.close()

    def test_create_keyspace(self):
        query = "SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name='financial_data'"
        result = self.db.session.execute(query)
        self.assertTrue(result.one())

    def test_create_table(self):
        query = "SELECT table_name FROM system_schema.tables WHERE keyspace_name='financial_data' AND table_name='nasdaq_data'"
        result = self.db.session.execute(query)
        self.assertTrue(result.one())

    def test_insert_data(self):
        data = NasdaqData.create(
            symbol='AAPL',
            date='2023-01-01',
            open=150,
            high=155,
            low=145,
            close=152,
            volume=100000
        )
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
