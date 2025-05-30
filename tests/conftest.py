import os
import sys
import pytest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.database_mongo import MongoDBHandler
from app.database_mongo.config import Config

DB_PATH = "pokemon_card_data.db"


# @pytest.fixture(autouse=True)
def clean_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture(scope="function", autouse=True)
def clean_database_mongo():
    """
    Fixture to ensure the MongoDB database is cleared before each test.
    """
    handler = MongoDBHandler(uri=Config.MONGO_URI, db_name=Config.MONGO_DB_NAME)
    handler.connect()
    retries = 3
    for attempt in range(retries):
        try:
            handler.client.drop_database(Config.MONGO_DB_NAME)
            break  # Exit loop if successful
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)  # Wait before retrying
            else:
                print(f"Failed to drop database after {retries} attempts: {e}")
    try:
        handler.close_connection()
    except Exception as e:
        print(f"Error while closing connection: {e}")


# Deletes the database file before test run
clean_database()
