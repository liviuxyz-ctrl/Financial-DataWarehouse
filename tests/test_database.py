# tests/test_database.py
import unittest
import uuid
import datetime
from tests.base_test import BaseTest
from src.models import Asset, DataSource, FinancialData


class TestDatabase(BaseTest):
    def test_create_keyspace(self):
        query = "SELECT keyspace_name FROM system_schema.keyspaces WHERE keyspace_name='financial_data'"
        result = self.db.session.execute(query)
        self.assertTrue(result.one())

    def test_create_table(self):
        query = "SELECT table_name FROM system_schema.tables WHERE keyspace_name='financial_data' AND table_name='financial_data'"
        result = self.db.session.execute(query)
        self.assertTrue(result.one())

    def test_insert_data(self):
        asset = Asset.create(asset_id=uuid.uuid4(), name='Apple Inc.', type='Stock')
        source = DataSource.create(source_id=uuid.uuid4(), source_name='Nasdaq Data Link')
        data = FinancialData.create(
            asset_id=asset.asset_id,
            source_id=source.source_id,
            business_date='2023-01-01',
            system_time=datetime.datetime.now(),
            open=150,
            high=155,
            low=145,
            close=152,
            volume=100000
        )
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
