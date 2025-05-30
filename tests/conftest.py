import os
import pytest

DB_PATH = "pokemon_card_data.db"


# @pytest.fixture(autouse=True)
def clean_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


# Deletes the database file before test run
clean_database()
