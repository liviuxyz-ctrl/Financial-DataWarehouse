# tests/test_models.py
import unittest
from tests.base_test import BaseTest
from src.data.models import Asset, DataSource, FinancialData
import uuid


class TestModels(BaseTest):
    def test_asset_model(self):
        asset = Asset.create(asset_id=uuid.uuid4(), name='Apple Inc.', type='Stock')
        self.assertIsNotNone(asset)
        self.assertEqual(asset.name, 'Apple Inc.')

    def test_data_source_model(self):
        source = DataSource.create(source_id=uuid.uuid4(), source_name='Nasdaq Data Link')
        self.assertIsNotNone(source)
        self.assertEqual(source.source_name, 'Nasdaq Data Link')

    def test_financial_data_model(self):
        data = FinancialData.create(
            asset_id=uuid.uuid4(),
            source_id=uuid.uuid4(),
            business_date='2023-01-01',
            system_time=datetime.datetime.now(),
            open=150,
            high=155,
            low=145,
            close=152,
            volume=100000
        )
        self.assertIsNotNone(data)
        self.assertEqual(data.open, 150)


if __name__ == '__main__':
    unittest.main()
