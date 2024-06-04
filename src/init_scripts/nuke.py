# init_scripts/nuke.py
from cassandra.cluster import Cluster
from src.config.settings import Config


def nuke_keyspace():
    cluster = Cluster(Config.CASSANDRA_NODES, port=Config.CASSANDRA_PORT)
    session = cluster.connect()
    session.execute(f"DROP KEYSPACE IF EXISTS {Config.KEYSPACE_NAME}")
    cluster.shutdown()


if __name__ == "__main__":
    nuke_keyspace()
