# tests/test_nasdaq_api_client.py
import unittest
from unittest.mock import patch
from tests.base_test import BaseTest
from src.nasdaq_api_client import fetch_financial_data


class TestNasdaqApiClient(BaseTest):
    @patch('src.nasdaq_api_client.requests.get')
    def test_fetch_financial_data_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        expected_data = {'dataset': {'data': [['2023-01-01', 150, 155, 145, 152, 100000]]}}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        data = fetch_financial_data('AAPL')
        self.assertEqual(data, expected_data['dataset']['data'])

    @patch('src.nasdaq_api_client.requests.get')
    def test_fetch_financial_data_failure(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            fetch_financial_data('INVALID_SYMBOL')


if __name__ == '__main__':
    unittest.main()
