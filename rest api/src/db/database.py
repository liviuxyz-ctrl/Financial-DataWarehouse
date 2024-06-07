from cassandra.cqlengine.connection import setup
from config.settings import Config

def initialize_cassandra_connection():
    setup(Config.CASSANDRA_NODES, "financial_data", protocol_version=4)
