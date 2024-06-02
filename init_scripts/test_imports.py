from src.models import Asset, DataSource, create_financial_data_model, initialize_cassandra_connection


def test_imports():
    initialize_cassandra_connection()
    print("Imports are working fine.")


if __name__ == "__main__":
    test_imports()
