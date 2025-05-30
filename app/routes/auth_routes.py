from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.decorators import login_required
from app.database_mongo import MongoDBHandler

ERR_MSG_EMPTY_FORM = "Please fill in the form to register."
ERR_MSG_USERNAME_EXISTS = "Username already exists. Please choose a different one."
ERR_MSG_INVALID_CREDENTIALS = "Invalid username or password."
ERR_MSG_LOGIN_SUCCESS = "Login successful!"
ERR_MSG_REGISTRATION_SUCCESS = "Registration successful! Please log in."

auth_bp = Blueprint("auth", __name__)

mongo_handler = MongoDBHandler()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    response_message = ERR_MSG_EMPTY_FORM
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            mongo_handler.connect()
            db = mongo_handler.create_database()
            users_collection = db["users"]

            if users_collection.find_one({"username": username}):
                response_message = ERR_MSG_USERNAME_EXISTS
            else:
                users_collection.insert_one(
                    {
                        "username": username,
                        "pass_hash": generate_password_hash(password),
                    }
                )
                response_message = ERR_MSG_REGISTRATION_SUCCESS

            mongo_handler.close_connection()

    return response_message, 200


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        mongo_handler.connect()
        db = mongo_handler.create_database()
        users_collection = db["users"]

        user_data = users_collection.find_one({"username": username})
        mongo_handler.close_connection()

        if user_data and check_password_hash(user_data.get("pass_hash"), password):
            session["user_id"] = str(user_data.get("_id"))
            session["username"] = username
            return ERR_MSG_LOGIN_SUCCESS, 200

        return ERR_MSG_INVALID_CREDENTIALS, 200

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("auth.login"))
