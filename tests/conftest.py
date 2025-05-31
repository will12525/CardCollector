import os
import sys
import pytest
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.database.db_setter import DBCreator

DB_PATH = "pokemon_card_data.db"


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    # Initialize database
    with DBCreator() as db_connection:
        db_connection.create_db()


# Deletes the database file before test run
# clean_database()
