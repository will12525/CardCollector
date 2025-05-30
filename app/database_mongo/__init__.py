from pymongo import MongoClient
import logging
from app.database_mongo.config import Config


class MongoDBHandler:
    def __init__(self, uri=Config.MONGO_URI, db_name=Config.MONGO_DB_NAME):
        """
        Initialize the MongoDBHandler with a connection URI and database name.
        """
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self):
        """
        Connect to the MongoDB service.
        """
        try:
            self.client = MongoClient(self.uri)
            # Test the connection
            self.client.admin.command("ping")
            logging.info("Connected to MongoDB successfully.")
        except ConnectionError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise

    def create_database(self):
        """
        Create and return a new empty database.
        """
        if not self.client:
            raise RuntimeError("Not connected to MongoDB. Call connect() first.")
        self.db = self.client[self.db_name]
        logging.info(f"Database '{self.db_name}' created successfully.")
        return self.db

    def close_connection(self):
        """
        Close the connection to MongoDB.
        """
        if self.client:
            self.client.close()
            logging.info("MongoDB connection closed.")
