import os

class Config:
    CASSANDRA_NODES = os.getenv('CASSANDRA_NODES', 'localhost').split(',')
    CASSANDRA_PORT = int(os.getenv('CASSANDRA_PORT', 9042))
    KEYSPACE_NAME = os.getenv('KEYSPACE_NAME', 'financial_data')
    API_KEY = os.getenv('API_KEY', '78afpoi9yz-xWHLzZrGz')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '9EFW738B9I0BIOZN')
    BASE_URL = "http://localhost:8000/api/v1"
