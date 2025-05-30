import os
from flask import Flask
from flask_minify import minify
from app.database.db_setter import DBCreator
from app.utils.common_objects import DBType


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key"  # Replace with a strong key
    minify(app=app, html=True, js=True, cssless=True)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    # Initialize database
    with DBCreator(DBType.PHYSICAL) as db_connection:
        db_connection.create_db()

    # Register blueprints
    from app.routes import register_blueprints

    register_blueprints(app)

    return app
