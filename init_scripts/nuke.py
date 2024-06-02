# init_scripts/clear_keyspace.py
import os
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.metadata import KeyspaceMetadata

KEYSPACE = 'financial_data'


def clear_keyspace():
    # Enable schema management
    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = '1'

    # Initialize the connection to the Cassandra cluster
    cluster = Cluster(['localhost'], protocol_version=4)
    session = cluster.connect(KEYSPACE)

    # Set up cqlengine connection
    connection.set_session(session)

    # Fetch keyspace metadata
    keyspace_metadata = cluster.metadata.keyspaces[KEYSPACE]

    if not isinstance(keyspace_metadata, KeyspaceMetadata):
        raise ValueError(f"Keyspace {KEYSPACE} does not exist.")

    # Get list of all table names in the keyspace
    table_names = list(keyspace_metadata.tables.keys())

    # Drop all tables in the keyspace
    for table_name in table_names:
        session.execute(f"DROP TABLE IF EXISTS {KEYSPACE}.{table_name};")
        print(f"Table {table_name} has been dropped.")

    cluster.shutdown()


if __name__ == "__main__":
    clear_keyspace()
