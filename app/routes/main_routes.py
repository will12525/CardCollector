from flask import Blueprint, render_template, session, request, jsonify
import json
from app.utils.decorators import login_required
from app.database.db_getter import DatabaseHandler
from app.utils.common import can_user_open_pack, Pack
from app.utils import common_objects

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    with DatabaseHandler() as db_getter_connection:
        python_metadata = {
            "set_list": db_getter_connection.get_sets(),
        }
        iso_string = db_getter_connection.get_user_pack_time(
            session.get("username"), session.get("user_id")
        )
        (can_user, next_allowed_time) = can_user_open_pack(iso_string)
        python_metadata["next_allowed_time"] = next_allowed_time
    return render_template(
        "index.html", username=session.get("username"), python_metadata=python_metadata
    )


@main_bp.route("/get_set_card_list_html", methods=["POST"])
@login_required
def get_set_card_list_html():
    meta_data = {}
    print("----------------------get_set_card_list_html----------------------")
    if json_request := request.get_json():
        with DatabaseHandler() as db_getter_connection:
            print(json_request)
            set_name = json_request.get(
                common_objects.SET_NAME_COLUMN,
                common_objects.get_set_name_from_index(1),
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

    print(json.dumps(meta_data, indent=4))
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

        print(f"generate_pack: {json_request}")
        with DatabaseHandler() as db_getter_connection:
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
                    card[common_objects.CARD_ID_COLUMN] = card[common_objects.ID_COLUMN]
                    card[common_objects.USER_ID_COLUMN] = session.get("user_id")
                    db_getter_connection.set_have(card)
    if data:
        return render_template(
            "card_list_template_jinja.html",
            meta_data=data,
        )
    else:
        return jsonify({"next_allowed_time": next_allowed_time}), 200
