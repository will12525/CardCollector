# File: tests/test_mongo_db_handler.py

import pytest
from app.database_mongo import MongoDBHandler
from app.database_mongo.config import Config


# Python
@pytest.fixture(scope="function")
def mongo_handler():
    """
    Fixture to initialize and clean up the MongoDBHandler using Config data.
    """
    handler = MongoDBHandler(uri=Config.MONGO_URI, db_name=Config.MONGO_DB_NAME)
    handler.connect()
    yield handler
    try:
        handler.client.drop_database(
            Config.MONGO_DB_NAME
        )  # Cleanup test database first
    except Exception as e:
        print(f"Error while dropping database: {e}")
    finally:
        try:
            handler.close_connection()  # Close the connection after cleanup
        except Exception as e:
            print(f"Error while closing connection: {e}")


def test_connect(mongo_handler):
    """
    Test the connect method of MongoDBHandler.
    """
    assert mongo_handler.client is not None


def test_create_database(mongo_handler):
    """
    Test the create_database method of MongoDBHandler.
    """
    db = mongo_handler.create_database()
    # Create a collection to ensure the database is persisted
    db.create_collection("test_collection")
    assert db.name == Config.MONGO_DB_NAME
    assert Config.MONGO_DB_NAME in mongo_handler.client.list_database_names()


def test_close_connection(mongo_handler):
    """
    Test the close_connection method of MongoDBHandler.
    """
    mongo_handler.close_connection()
    assert mongo_handler.client is not None  # Client object should still exist
