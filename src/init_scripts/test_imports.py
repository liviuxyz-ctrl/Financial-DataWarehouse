# init_scripts/test_imports.py
from src.data.models import Asset, DataSource
from src.data.database import DatabaseManager


def test_imports():
    db = DatabaseManager()
    db.create_keyspace()
    db.create_tables()
    db.close()
    print("Imports are working fine.")


if __name__ == "__main__":
    test_imports()
