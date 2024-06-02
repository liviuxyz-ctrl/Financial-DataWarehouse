# tests/test_data_processor.py
import unittest
from src.data_processor import transform_data


class TestDataProcessor(unittest.TestCase):
    def test_transform_data(self):
        raw_data = [
            ['2023-01-01', 150, 155, 145, 152, 100000],
            ['2023-01-02', 153, 158, 149, 155, 110000]
        ]
        expected_output = [
            {'symbol': 'AAPL', 'date': '2023-01-01', 'open': 150, 'high': 155, 'low': 145, 'close': 152,
             'volume': 100000},
            {'symbol': 'AAPL', 'date': '2023-01-02', 'open': 153, 'high': 158, 'low': 149, 'close': 155,
             'volume': 110000}
        ]
        result = transform_data('AAPL', raw_data)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
