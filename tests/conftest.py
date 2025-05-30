import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


DB_PATH = "pokemon_card_data.db"


# @pytest.fixture(autouse=True)
def clean_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


# Deletes the database file before test run
clean_database()
