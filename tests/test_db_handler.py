# File: tests/test_mongo_db_handler.py

import pytest
from app.database.db_setter import DBCreator


# def test_connect(mongo_handler):
#     """
#     Test the connect method of MongoDBHandler.
#     """
#     assert mongo_handler.client is not None
#
#
# def test_create_database(mongo_handler):
#     """
#     Test the create_database method of MongoDBHandler.
#     """
#     db = mongo_handler.create_database()
#     # Create a collection to ensure the database is persisted
#     db.create_collection("test_collection")
#     assert db.name == Config.MONGO_DB_NAME
#     assert Config.MONGO_DB_NAME in mongo_handler.client.list_database_names()
#
#
# def test_close_connection(mongo_handler):
#     """
#     Test the close_connection method of MongoDBHandler.
#     """
#     mongo_handler.close_connection()
#     assert mongo_handler.client is not None  # Client object should still exist
