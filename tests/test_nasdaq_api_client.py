# tests/test_nasdaq_api_client.py
import unittest
from unittest.mock import patch
from src.nasdaq_api_client import fetch_financial_data


class TestNasdaqApiClient(unittest.TestCase):
    @patch('src.nasdaq_api_client.requests.get')
    def test_fetch_financial_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'dataset': {'data': [['2023-01-01', 150, 155, 145, 152, 100000]]}
        }
        result = fetch_financial_data('AAPL')
        self.assertEqual(result, [['2023-01-01', 150, 155, 145, 152, 100000]])

    @patch('src.nasdaq_api_client.requests.get')
    def test_fetch_financial_data_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {
            'quandl_error': {'message': 'Dataset not found'}
        }
        with self.assertRaises(Exception) as context:
            fetch_financial_data('AAPL')
        self.assertIn('Dataset not found', str(context.exception))


if __name__ == '__main__':
    unittest.main()
