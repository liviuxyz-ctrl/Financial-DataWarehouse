# init_scripts/clear_data.py
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from src.config.settings import Config


def clear_data():
    cluster = Cluster(Config.CASSANDRA_NODES, port=Config.CASSANDRA_PORT)
    session = cluster.connect(Config.KEYSPACE_NAME)
    connection.set_session(session)
    session.execute(f"TRUNCATE TABLE {Config.KEYSPACE_NAME}.financial_data")
    session.execute(f"TRUNCATE TABLE {Config.KEYSPACE_NAME}.asset")
    session.execute(f"TRUNCATE TABLE {Config.KEYSPACE_NAME}.data_source")
    cluster.shutdown()


if __name__ == "__main__":
    clear_data()
