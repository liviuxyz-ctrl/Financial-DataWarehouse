# tests/test_data_processor.py
import unittest
from tests.base_test import BaseTest
from src.data_processor import transform_data, store_financial_data
from src.models import FinancialData
import uuid


class TestDataProcessor(BaseTest):
    def test_transform_data(self):
        raw_data = [
            ['2023-01-01', 150, 155, 145, 152, 100000],
            ['2023-01-02', 152, 158, 150, 157, 150000]
        ]
        transformed = transform_data('AAPL', raw_data)
        self.assertEqual(len(transformed), 2)
        self.assertEqual(transformed[0]['symbol'], 'AAPL')
        self.assertEqual(transformed[0]['date'], '2023-01-01')

    def test_store_financial_data(self):
        asset_id = uuid.uuid4()
        source_id = uuid.uuid4()
        data = [
            {'symbol': 'AAPL', 'date': '2023-01-01', 'open': 150, 'high': 155, 'low': 145, 'close': 152,
             'volume': 100000},
            {'symbol': 'AAPL', 'date': '2023-01-02', 'open': 152, 'high': 158, 'low': 150, 'close': 157,
             'volume': 150000}
        ]
        store_financial_data(asset_id, source_id, data)
        result = FinancialData.objects.filter(asset_id=asset_id).all()
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
