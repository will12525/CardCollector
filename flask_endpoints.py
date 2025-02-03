import pathlib
import os
from enum import Enum
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
    Response,
)
import datetime

from flask_minify import minify

import database_handler.db_access
from database_handler import common_objects
from database_handler.common_objects import DBType
from database_handler.db_getter import DatabaseHandler
from database_handler.db_setter import DBCreator
from pack_generator import Pack
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# from database_handler.input_file_parser import load_set_data_dir

# USERS
# There are two users
#       Willow
#               Can update all states
#               Can view HAVE
#               Can view WANT
#       Tori
#               Can update GIFT
#               Can view all cards
# Be able to change the current user
#
# VIEWS
# ALWAYS Hide gifted cards
#       Unless Tori is User
# Display a list of all pokemon cards
# Display all cards by set
#       Be able to change the viewed set

# CARDS
# Have a Have, Want, Gift Mark
# Be able to change want to have
#       Unless Tori is user
# Be able to mark a card as gifted
#       Unless Willow is user
#       Be able to remove gifted mark


app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "your_secret_key"  # Replace with a strong, randomly generated key
)
minify(app=app, html=True, js=True, cssless=True)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


class APIEndpoints(Enum):
    MAIN = "/"
    GET_SET_CARD_LIST = "/get_set_card_list"
    GET_SET_CARD_LIST_HTML = "/get_set_card_list_html"
    UPDATE_HAVE = "/update_have"
    UPDATE_WANT = "/update_want"
    GIFTED = "/gifted"
    UPDATE_CARD_INDEX = "/update_card_index"
    GENERATE_PACK = "/generate_pack"
    REGISTER = "/new_user"
    LOGIN = "/login"
    LOGOUT = "/logout"


DB_PATH = database_handler.db_access.DBConnection.MEDIA_METADATA_DB_NAME


# Create an empty DB
def setup_db():
    if not os.path.exists(DB_PATH):
        with DBCreator(DBType.PHYSICAL) as db_connection:
            db_connection.create_db()


# Decorator to protect routes that require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/register", methods=["GET", "POST"])
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
                db_request[common_objects.USER_PASS_COLUMN] = generate_password_hash(
                    db_request["password"]
                )
                if db_getter_connection.add_user(db_request):
                    response_message = "Registration successful! Please log in."

    return response_message, 200


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with DatabaseHandler() as db_getter_connection:
            if user_data := db_getter_connection.get_user_hash(
                {
                    "user_name": username,
                }
            ):
                if check_password_hash(
                    user_data.get(common_objects.USER_PASS_COLUMN), password
                ):
                    session["user_id"] = user_data.get(common_objects.ID_COLUMN)
                    session["username"] = username
                    return "Login Successful!", 200

        return "Invalid username or password.", 200

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route(APIEndpoints.MAIN.value)
@login_required
def index():
    with DatabaseHandler() as db_getter_connection:
        python_metadata = {
            "set_list": db_getter_connection.get_sets(),
        }
    return render_template(
        "index.html", username=session.get("username"), python_metadata=python_metadata
    )


@app.route(APIEndpoints.GET_SET_CARD_LIST_HTML.value, methods=["POST"])
@login_required
def get_set_card_list_html():
    meta_data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            print(json_request)
            meta_data.update(
                db_getter_connection.query_collection(
                    json_request.get(
                        common_objects.SET_NAME_COLUMN,
                        common_objects.get_set_name_from_index(1),
                    ),
                    json_request.get("filter_str"),
                    json_request.get("card_name_search_query"),
                    json_request.get("filter_ownership"),
                    json_request.get("card_season_search_query"),
                    session.get("user_id"),
                )
            )
    print(meta_data)
    return render_template(
        "card_list_template_jinja.html",
        meta_data=meta_data,
    )


@app.route(APIEndpoints.GET_SET_CARD_LIST.value, methods=["POST"])
@login_required
def get_set_card_list():
    data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            data.update(
                db_getter_connection.query_collection(
                    json_request.get(common_objects.SET_NAME_COLUMN),
                    json_request.get("filter_str"),
                    json_request.get("card_name_search_query"),
                    json_request.get("filter_ownership"),
                    json_request.get("card_season_search_query"),
                    session.get("user_id"),
                )
            )
            data["set_list"] = db_getter_connection.get_sets()
    return jsonify(data), 200


def can_user_open_pack(db_getter_connection, db_request):
    iso_string = db_getter_connection.get_user_pack_time(db_request).get(
        common_objects.LAST_PACK_OPEN_TIME_COLUMN
    )
    if not iso_string:
        return True, None
    last_open_time = datetime.datetime.fromisoformat(
        iso_string.replace("Z", "+00:00")
    )  # Handle UTC and other timezone strings
    current_time = datetime.datetime.now(datetime.UTC)

    time_difference = current_time - last_open_time

    if time_difference >= datetime.timedelta(hours=1):
        return True, None
    else:
        remaining_time = datetime.timedelta(hours=1) - time_difference
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        iso_duration = (
            f"{int(hours)}H:{int(minutes)}M:{int(seconds)}S"  # ISO8601 duration format
        )
        return False, iso_duration


@app.route(APIEndpoints.GENERATE_PACK.value, methods=["POST"])
@login_required
def generate_pack():
    data = {}
    wait_time = ""

    if json_request := request.get_json():
        db_request = {
            "set_name": json_request.get("set_name"),
            "user_id": session.get("user_id"),
            "user_name": session.get("username"),
        }

        print(f"generate_pack: {json_request}")
        with DatabaseHandler() as db_getter_connection:
            (can_user, wait_time) = can_user_open_pack(db_getter_connection, db_request)
            if can_user:
                db_getter_connection.set_user_pack_time(db_request)
                set_card_list = db_getter_connection.get_all_set_card_data(db_request)
                pack = Pack(set_card_list)
                data["set_card_list"] = pack.open()
                data["set_list"] = db_getter_connection.get_sets()
                # Update user collection with the new pack data
                for card in data["set_card_list"]:
                    db_getter_connection.set_have(
                        {
                            common_objects.OWN_COUNT_COLUMN: 1,
                            common_objects.CARD_ID_COLUMN: card.get(
                                common_objects.ID_COLUMN
                            ),
                            common_objects.USER_ID_COLUMN: session.get("user_id"),
                        }
                    )
    if data:
        return render_template(
            "card_list_template_jinja.html",
            meta_data=data,
        )
    else:
        return f"Please wait: {wait_time}", 200


@app.route(APIEndpoints.UPDATE_HAVE.value, methods=["POST"])
def update_have():
    data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            db_getter_connection.set_have(json_request)
    return jsonify(data), 200


@app.route(APIEndpoints.UPDATE_WANT.value, methods=["POST"])
def update_want():
    data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            db_getter_connection.set_want(json_request)
    return jsonify(data), 200


@app.route(APIEndpoints.GIFTED.value, methods=["POST"])
def gifted():
    data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            db_getter_connection.gifted(json_request)
    return jsonify(data), 200


@app.route(APIEndpoints.UPDATE_CARD_INDEX.value, methods=["POST"])
def update_card_index():
    data = {}
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            print(json_request)
            db_getter_connection.set_card_index(json_request)
    return jsonify(data), 200


if __name__ == "__main__":
    setup_db()
    print("--------------------Running Main--------------------")
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
