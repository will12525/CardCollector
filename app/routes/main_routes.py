from flask import Blueprint, render_template, session, request, jsonify
import json
from app.utils.decorators import login_required
from app.database.db_getter import DatabaseHandler
from app.utils.common import can_user_open_pack, Pack
from app.utils.common_objects import get_set_name_from_index

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    print(session.get("username"), "----------------------index----------------------")
    db_getter_connection = DatabaseHandler()
    db_getter_connection.open()
    python_metadata = {
        "set_list": db_getter_connection.get_sets(),
    }
    iso_string = db_getter_connection.get_user_pack_time(
        session.get("username"), session.get("user_id")
    )
    (can_user, next_allowed_time) = can_user_open_pack(iso_string)
    python_metadata["next_allowed_time"] = next_allowed_time
    db_getter_connection.close()

    return render_template(
        "index.html", username=session.get("username"), python_metadata=python_metadata
    )


@main_bp.route("/get_set_card_list_html", methods=["POST"])
@login_required
def get_set_card_list_html():
    meta_data = {}
    print("----------------------get_set_card_list_html----------------------")
    if json_request := request.get_json():
        db_getter_connection = DatabaseHandler()
        db_getter_connection.open()
        print(session.get("username"), json_request)
        set_name = json_request.get(
            "set_name",
            get_set_name_from_index(1),
        )
        meta_data.update(
            db_getter_connection.query_collection(
                set_name,
                json_request.get("filter_str"),
                json_request.get("card_name_search_query"),
                json_request.get("filter_ownership"),
                session.get("user_id"),
            )
        )
        db_request = {
            "set_name": set_name,
            "user_id": session.get("user_id"),
            "user_name": session.get("username"),
        }
        db_getter_connection.set_user_last_set(db_request)
        db_getter_connection.close()

    # print(json.dumps(meta_data, indent=4))
    return render_template(
        "card_list_template_jinja.html",
        meta_data=meta_data,
    )


@main_bp.route("/generate_pack", methods=["POST"])
@login_required
def generate_pack():
    data = {}
    next_allowed_time = None

    if json_request := request.get_json():
        db_request = {
            "set_name": json_request.get("set_name"),
            "user_id": session.get("user_id"),
            "user_name": session.get("username"),
        }

        print(
            f"User: {session.get("username")} requested generate_pack: {json_request}"
        )

        db_getter_connection = DatabaseHandler()
        db_getter_connection.open()
        iso_string = db_getter_connection.get_user_pack_time(
            session.get("username"), session.get("user_id")
        )
        (can_user, next_allowed_time) = can_user_open_pack(iso_string)
        if can_user:
            db_getter_connection.set_user_pack_time(
                session.get("username"), session.get("user_id")
            )
            set_card_list = db_getter_connection.get_all_set_card_data(db_request)
            pack = Pack(set_card_list)
            data["set_card_list"] = pack.open()
            # Update user collection with the new pack data
            for card in data["set_card_list"]:
                card["card_id"] = card["id"]
                card["user_id"] = session.get("user_id")
                db_getter_connection.set_have(card)
        db_getter_connection.close()
    if data:
        return render_template(
            "card_list_template_jinja.html",
            meta_data=data,
        )
    else:
        return jsonify({"next_allowed_time": next_allowed_time}), 200
