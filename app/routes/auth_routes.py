from flask import Blueprint, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.decorators import login_required
from app.database.db_getter import DatabaseHandler

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    response_message = ""
    if request.method == "POST":
        db_request = {
            "user_name": request.form["username"],
            "password": request.form["password"],
        }

        with DatabaseHandler() as db_getter_connection:
            if db_getter_connection.get_user_id(db_request):
                response_message = (
                    "Username already exists. Please choose a different one."
                )
            else:
                db_request["user_pass_hash"] = generate_password_hash(
                    db_request["password"]
                )
                if db_getter_connection.add_user(db_request):
                    response_message = "Registration successful! Please log in."

    return response_message, 200


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
        with DatabaseHandler() as db_getter_connection:
            if user_data := db_getter_connection.get_user_hash(
                {
                    "user_name": username,
                }
            ):
                if check_password_hash(user_data.get("user_pass_hash"), password):
                    session["user_id"] = user_data.get("id")
                    session["username"] = username
                    return "Login Successful!", 200

        return "Invalid username or password.", 200

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("auth.login"))
