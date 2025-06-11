import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.database.db_getter import DatabaseHandler

DB_PATH = "pokemon_card_data.db"


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    # Initialize database
    db_getter_connection = DatabaseHandler()
    db_getter_connection.open()
    db_getter_connection.create_db()
    db_getter_connection.close()
