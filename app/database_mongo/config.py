# config.py

import os


class Config:
    # MongoDB connection URI for local development
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    # Name of the database
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "my_database")
