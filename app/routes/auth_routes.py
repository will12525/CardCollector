from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.decorators import login_required
from app.database.db_getter import DatabaseHandler

ERR_MSG_EMPTY_FORM = "Please fill in the form to register."
ERR_MSG_USERNAME_EXISTS = "Username already exists. Please choose a different one."
ERR_MSG_INVALID_CREDENTIALS = "Invalid username or password."
ERR_MSG_LOGIN_SUCCESS = "Login successful!"
ERR_MSG_REGISTRATION_SUCCESS = "Registration successful! Please log in."
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    response_message = ERR_MSG_EMPTY_FORM
    if request.method == "POST":
        db_request = {
            "user_name": request.form["username"],
            "password": request.form["password"],
        }

        db_getter_connection = DatabaseHandler()
        db_getter_connection.open()
        if db_getter_connection.get_user_id(db_request):
            response_message = ERR_MSG_USERNAME_EXISTS
        else:
            db_request["user_pass_hash"] = generate_password_hash(
                db_request["password"]
            )
            if db_getter_connection.add_user(db_request):
                response_message = ERR_MSG_REGISTRATION_SUCCESS
        db_getter_connection.close()

    return response_message, 200


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db_getter_connection = DatabaseHandler()
        db_getter_connection.open()
        if user_data := db_getter_connection.get_user_hash({"user_name": username}):
            if check_password_hash(user_data.get("user_pass_hash"), password):
                session["user_id"] = user_data.get("id")
                session["username"] = username
                print("User logged in:", username)
                db_getter_connection.close()
                return ERR_MSG_LOGIN_SUCCESS, 200
        db_getter_connection.close()
        return ERR_MSG_INVALID_CREDENTIALS, 200

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("auth.login"))
