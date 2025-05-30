from flask import Blueprint, request, jsonify, render_template, session
import json
from app.database.db_getter import DatabaseHandler
from app.utils.decorators import login_required
from app.utils import common_objects

deck_bp = Blueprint("deck", __name__)


def can_user_add_card_to_deck(db_getter_connection, user_id, deck_id, card_id):
    print("----------------------can_user_add_card_to_deck----------------------")
    # 4 unique cards per deck unless energy card
    card_count = db_getter_connection.get_deck_cards_card_count(deck_id, card_id)
    card_info = db_getter_connection.get_card_info(card_id)
    deck_stats = db_getter_connection.get_deck_stats(deck_id)
    print(card_info)
    print(deck_stats)
    print(card_count)
    if (
        card_count
        and card_count >= 4
        and card_info.get(common_objects.CARD_CLASS_COLUMN) != "energy"
    ):
        return False
    elif deck_stats.get("card_count") and deck_stats.get("card_count") >= 60:
        return False
    return True


@deck_bp.route("/get_deck_data_html", methods=["POST"])
@login_required
def get_deck_data_html():
    meta_data = {"user_id": session.get("user_id")}
    print("----------------------get_deck_data_html----------------------")
    if json_request := request.get_json():
        action_id = json_request.get("action_id")
        deck_name = json_request.get("deck_name")
        deck_id = json_request.get("deck_id")
        card_id = json_request.get("card_id")
        card_list = json_request.get("card_list", [])
        if deck_name:
            deck_name = deck_name.strip()
        meta_data["deck_id"] = deck_id

        with DatabaseHandler() as db_getter_connection:
            print(f"json_request: {json.dumps(json_request, indent=4)}")
            if action_id == common_objects.DeckBuilderActions.UPDATE_DECK.value:
                if deck_id:
                    print("Updating Deck")
                    db_getter_connection.update_deck(
                        deck_name,
                        deck_id,
                        session.get("user_id"),
                    )
                    meta_data["deck_id"] = deck_id
                else:
                    print("Adding Deck")
                    meta_data["deck_id"] = db_getter_connection.create_deck(
                        session.get("user_id"),
                        deck_name,
                        card_list,
                    )
            elif (
                action_id == common_objects.DeckBuilderActions.ADD_CARD.value
            ) and can_user_add_card_to_deck(
                db_getter_connection,
                session.get("user_id"),
                deck_id,
                card_id,
            ):
                print("Adding Card")
                db_getter_connection.add_card_to_deck(
                    session.get("user_id"),
                    deck_id,
                    card_id,
                )
            elif action_id == common_objects.DeckBuilderActions.REMOVE_CARD.value:
                print("Removing Card")
                db_getter_connection.remove_card_from_deck(card_id, deck_id)
            elif action_id == common_objects.DeckBuilderActions.LOAD_DECK.value:
                pass
            else:
                print("Unknown action")
                return jsonify({"error": "Unknown action"}), 400

            meta_data["deck_name_list"] = db_getter_connection.get_user_decks(
                session.get("user_id")
            )
            selected_deck_id = meta_data.get("deck_id")
            if not selected_deck_id and len(meta_data["deck_name_list"]) > 0:
                selected_deck_id = meta_data["deck_name_list"][0].get(
                    common_objects.ID_COLUMN
                )

            if selected_deck_id:
                meta_data["deck_id"] = selected_deck_id
                meta_data.update(
                    db_getter_connection.get_deck_info(
                        meta_data["deck_id"], session.get("user_id")
                    )
                )
                meta_data["deck_card_list"] = db_getter_connection.get_deck_cards(
                    meta_data["deck_id"], session.get("user_id")
                )
                meta_data["deck_stats"] = db_getter_connection.get_deck_stats(
                    meta_data["deck_id"]
                )

    print(f"meta_data: {json.dumps(meta_data.get("deck_card_list"), indent=4)}")
    return render_template(
        "deck_template_jinja.html",
        meta_data=meta_data,
    )
