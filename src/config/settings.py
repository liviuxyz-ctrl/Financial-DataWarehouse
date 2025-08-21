# src/config/settings.py
import os

class Config:
    CASSANDRA_NODES = os.getenv('CASSANDRA_NODES', 'localhost').split(',')
    CASSANDRA_PORT = int(os.getenv('CASSANDRA_PORT', 9042))
    KEYSPACE_NAME = os.getenv('KEYSPACE_NAME', 'financial_data')
    API_KEY = os.getenv('API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

    if API_KEY is None:
        raise EnvironmentError("API_KEY environment variable not set")
    if ALPHA_VANTAGE_API_KEY is None:
        raise EnvironmentError("ALPHA_VANTAGE_API_KEY environment variable not set")

