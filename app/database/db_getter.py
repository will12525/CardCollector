import datetime
from app.utils.common_objects import get_set_card_count
from app.database.db_access import DBConnection
import app.database.db_queries as queries


def get_sort_order(filter_str):
    if filter_str == "Card Index":
        return queries.sort_index_asc
    elif filter_str == "Card Index Reverse":
        return queries.sort_index_desc
    elif filter_str == "A-Z":
        return queries.sort_name_alpha_asc
    elif filter_str == "Z-A":
        return queries.sort_name_alpha_desc
    elif filter_str == "Have":
        return queries.sort_own_desc
    else:
        return ""


class DatabaseHandler(DBConnection):

    def create_db(self):
        db_version = self.check_db_version()
        print(f"DB COMPARE: Current: {db_version}, Expected: {self.VERSION}")
        if self.VERSION != db_version:
            # Run db update procedure
            self.update_database(db_version)
        # elif self.VERSION == db_version:
        #     pass
        else:
            db_table_creation_script = [
                queries.sql_create_set_info_table,
                queries.sql_create_card_info_table,
                queries.sql_create_user_info_table,
                queries.sql_create_user_collection_table,
                queries.sql_create_deck_info_table,
                queries.sql_create_deck_cards_info_table,
                queries.sql_create_ban_info_table,
            ]
            self.execute_db_script(db_table_creation_script)

    def set_card_metadata(self, card_data) -> int:
        return self.add_data_to_db(queries.sql_insert_card_info_table, card_data)

    def add_set_card_data(self, set_data):
        set_data.set_id = self.set_set_data(set_data.to_dict())

        for card in set_data.card_dict.values():
            card.set_id = set_data.set_id
            self.set_card_metadata(card.to_dict())

    def insert_card(self, card):
        card["set_id"] = self.get_set_id_from_name(card.get("set_name"))
        print(card)
        self.set_card_metadata(card)

    def set_set_data(self, set_data):
        return self.add_data_to_db(queries.sql_insert_set_info_table, set_data)

    def get_set_id_from_name(self, set_name) -> dict:
        return self.get_row_id(
            queries.get_set_id_from_name,
            {"set_name": set_name},
        )

    def update_database(self, current_version):
        """Updates the database schema to the latest version."""
        if current_version == 1:
            current_version = 2
            print(f"Updating database to version {current_version}...")
            query_list = [
                queries.sql_create_deck_info_table,
                queries.sql_create_deck_cards_info_table,
                queries.sql_create_ban_info_table,
                f"ALTER TABLE card_info ADD COLUMN attack_info TEXT DEFAULT '';",
                f"ALTER TABLE card_info ADD COLUMN energy_cost TEXT DEFAULT '';",
                f"ALTER TABLE card_info ADD COLUMN card_text TEXT DEFAULT '';",
                f"ALTER TABLE user_info ADD COLUMN last_set_name TEXT DEFAULT '';"
                f"ALTER TABLE user_info ADD COLUMN last_deck_id INTEGER;"
                f"UPDATE version_info SET version = {current_version} WHERE id = 1;",
            ]
            self.execute_db_script(query_list)
            print(f"Database updated to version {current_version}.")

    def get_all_card_data(self):
        return self.get_data_from_db(queries.get_all_card_data)

    def get_all_set_card_data(self, params):
        # print(params)
        return self.get_data_from_db(
            queries.get_all_set_card_data,
            params,
        )

    def query_collection(
        self,
        set_name,
        filter_str,
        card_name_search_query,
        filter_ownership,
        user_id,
    ):
        print(set_name)
        ret_data = {}
        params = {"user_id": user_id}
        where_clauses = []
        where_clause = ""
        sort_order = get_sort_order(filter_str)

        if set_name:
            where_clauses.append(f"set_name=:set_name")
            params["set_name"] = set_name

        if card_name_search_query:
            where_clauses.append(f"card_name LIKE :card_name_search_query")
            params["card_name_search_query"] = f"%{card_name_search_query}%"

        if filter_ownership and filter_ownership == "have":
            where_clauses.append(f"own_count>0")

        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)
        ret_data["set_card_list"] = self.get_data_from_db(
            f"SELECT *, user_collection.id AS user_collection_id {queries.collection_base_query} {where_clause} {sort_order};",
            params,
        )
        ret_data.update(
            self.get_data_from_db_first_result(
                f"SELECT COUNT(own_count) AS count_have {queries.collection_base_query} {where_clause} {sort_order};",
                params,
            )
        )
        if set_name:
            ret_data["set_name"] = set_name
            ret_data["count_cards"] = get_set_card_count(set_name)
            if ret_data.get("count_have", 0) > 0:
                ret_data["percent_complete"] = round(
                    (ret_data["count_have"] / ret_data["count_cards"]) * 100
                )
            else:
                ret_data["percent_complete"] = 0
        return ret_data

    def get_sets(self):
        return self.get_data_from_db(queries.get_sets)

    def get_set_card_count(self, params):
        return self.get_row_item(
            queries.get_set_card_count,
            params,
            "set_card_count",
        )

    def get_card_from_id(self, params):
        return self.get_data_from_db_first_result(
            queries.get_card_from_id,
            params,
        )

    def get_card_info(self, card_id):
        return self.get_data_from_db_first_result(
            queries.get_card_info,
            {"card_id": card_id},
        )

    def get_all_ids(self):
        return self.get_data_from_db(queries.get_all_ids)

    def get_card_with_set_index(self, params):
        return self.get_data_from_db_first_result(
            queries.get_card_with_set_index,
            params,
        )

    def set_have(self, params):
        # Update an existing row
        affected_row = self.add_data_to_db(
            queries.increment_card_in_user_collection,
            params,
        )
        # If an existing row doesn't exist, add a new row
        if affected_row is None:
            self.add_data_to_db(
                queries.add_card_to_user_collection,
                params,
            )
            params["new"] = True

        # Update the parameters object to include the current own count
        params["own_count"] = self.get_row_item(
            queries.get_card_in_user_collection_count, params, "own_count"
        )

    def reset_users(self):
        return self.get_data_from_db(queries.delete_users)

    def reset_decks(self):
        self.get_data_from_db(queries.delete_deck_cards)
        self.get_data_from_db(queries.delete_deck_info)

    def search_card_names(self, card_name):
        return self.get_data_from_db(
            queries.search_card_names,
            (f"%{card_name}%",),
        )

    def generate_random_pack(self, params):
        return self.get_data_from_db(
            queries.generate_random_pack,
            params,
        )

    def generate_pack_from_set(self, params):
        return self.get_data_from_db(
            queries.generate_pack_from_set,
            params,
        )

    def add_user(self, params):
        return self.add_data_to_db(queries.sql_insert_user_info_table, params)

    def get_user_id(self, params):
        return self.get_row_id(
            queries.get_user_id,
            params,
        )

    def user_login(self, params):
        return self.get_row_id(
            queries.user_login,
            params,
        )

    def get_user_hash(self, params):
        return self.get_data_from_db_first_result(
            queries.get_user_hash,
            params,
        )

    def set_user_pack_time(self, username, user_id):
        return self.add_data_to_db(
            queries.set_user_pack_time,
            {
                "id": user_id,
                "user_name": username,
                "last_pack_open_time": datetime.datetime.now(datetime.UTC).isoformat(),
            },
        )

    def get_user_pack_time(self, username, user_id):
        return self.get_row_item(
            queries.get_user_pack_time,
            {"id": user_id, "user_name": username},
            "last_pack_open_time",
        )

    def set_user_last_set(self, params):
        return self.add_data_to_db(
            queries.set_user_last_set,
            params,
        )

    def add_card_to_deck(self, user_id, deck_id, card_id):
        """
        Adds a card to the deck. If the card already exists, increments its count.
        """
        self.add_data_to_db(
            queries.add_card_to_deck,
            {
                "user_id": user_id,
                "deck_id": deck_id,
                "card_id": card_id,
            },
        )

    def remove_card_from_deck(self, card_id, deck_id):
        """
        Removes a card from the deck by decrementing its count. If the count reaches 0, the card is removed from the deck.
        """
        params = {
            "card_id": card_id,
            "deck_id": deck_id,
        }
        self.add_data_to_db(
            queries.remove_card_from_deck,
            params,
        )
        self.add_data_to_db(queries.decrement_card_from_deck, params)

    def create_deck(self, user_id, deck_name, card_list):
        deck_id = self.add_data_to_db(
            queries.create_deck,
            {"deck_name": deck_name, "user_id": user_id},
        )
        print(f"New Deck ID: {deck_id}, Deck Name: {deck_name}")
        for card_id in card_list:
            self.add_card_to_deck(user_id, deck_id, card_id)
        return deck_id

    def update_deck(self, deck_name, deck_id, user_id):
        self.add_data_to_db(
            queries.update_deck,
            {"deck_name": deck_name, "deck_id": deck_id, "user_id": user_id},
        )

    def get_user_decks(self, user_id):
        return self.get_data_from_db(
            queries.get_user_decks,
            {"user_id": user_id},
        )

    def get_deck_cards(self, deck_id, user_id):
        return self.get_data_from_db(
            queries.get_deck_cards,
            {"deck_id": deck_id, "user_id": user_id},
        )

    def get_deck_cards_card_count(self, deck_id, card_id):
        return self.get_row_item(
            queries.get_deck_cards_card_count,
            {"deck_id": deck_id, "card_id": card_id},
            "card_count",
        )

    def get_deck_card_stat(self, card_column, deck_id):
        return self.get_data_from_db(
            f"""
                    SELECT
                    card_info.{card_column},
                    SUM(deck_cards.card_count) AS card_count
                    FROM deck_cards
                    JOIN card_info ON deck_cards.card_id = card_info.id
                    WHERE deck_cards.deck_id = :deck_id
                    GROUP BY card_info.{card_column};
                """,
            {"deck_id": deck_id},
        )

    def get_deck_card_count(self, deck_id):
        return self.get_row_item(
            queries.get_deck_card_count,
            {"deck_id": deck_id},
            "card_count",
        )

    def get_deck_info(self, deck_id, user_id):
        return self.get_data_from_db_first_result(
            queries.get_deck_info,
            {"deck_id": deck_id, "user_id": user_id},
        )

    def get_deck_stats(self, deck_id):
        return {
            "card_count": self.get_deck_card_count(deck_id),
            "card_classes": self.get_deck_card_stat("card_class", deck_id),
            "card_types": self.get_deck_card_stat("card_type", deck_id),
        }
