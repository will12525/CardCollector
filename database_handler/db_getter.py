import json
import pathlib
import datetime
from . import common_objects
from .db_access import DBConnection


def load_js_file(filename):
    if filename:
        file_path = pathlib.Path(filename)
        if file_path.is_file():
            with open(filename, mode="r") as f_in:
                try:
                    return json.load(f_in)
                except ValueError:
                    pass
    return {}


def save_js_file(filename, content):
    with open(filename, mode="w") as f_out:
        f_out.write(json.dumps(content, indent=4))


class DatabaseHandler(DBConnection):
    def get_all_card_data(self):
        return self.get_data_from_db(
            f"SELECT * FROM {common_objects.CARD_INFO_TABLE} INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN};"
        )

    def get_all_set_card_data(self, params):
        # print(params)
        return self.get_data_from_db(
            f"SELECT * FROM {common_objects.CARD_INFO_TABLE} INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN} LEFT JOIN {common_objects.USER_COLLECTION_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.ID_COLUMN} = {common_objects.USER_COLLECTION_TABLE}.{common_objects.CARD_ID_COLUMN} AND {common_objects.USER_COLLECTION_TABLE}.{common_objects.USER_ID_COLUMN} = :{common_objects.USER_ID_COLUMN} WHERE {common_objects.SET_NAME_COLUMN}=:{common_objects.SET_NAME_COLUMN};",
            params,
        )

    SORT_ALPHABETICAL = "GLOB '[A-Za-z]*'"
    BASE_QUERY = f"FROM {common_objects.CARD_INFO_TABLE} INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN} LEFT JOIN {common_objects.USER_COLLECTION_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.ID_COLUMN} = {common_objects.USER_COLLECTION_TABLE}.{common_objects.CARD_ID_COLUMN} AND {common_objects.USER_COLLECTION_TABLE}.{common_objects.USER_ID_COLUMN} = :{common_objects.USER_ID_COLUMN}"

    def get_sort_order(self, filter_str):
        sort_order = ""
        if filter_str == "Sets":
            sort_order = f"ORDER BY {common_objects.SET_INFO_TABLE}.{common_objects.SET_INDEX_COLUMN} ASC, {common_objects.CARD_INFO_TABLE}.{common_objects.CARD_INDEX_COLUMN} NULLS LAST, {common_objects.CARD_NAME_COLUMN}"
        elif filter_str == "Sets Reverse":
            sort_order = f"ORDER BY {common_objects.SET_INFO_TABLE}.{common_objects.SET_INDEX_COLUMN} DESC, {common_objects.CARD_INFO_TABLE}.{common_objects.CARD_INDEX_COLUMN} DESC NULLS LAST, {common_objects.CARD_NAME_COLUMN} DESC"
        elif filter_str == "Card Index":
            sort_order = f"ORDER BY {common_objects.CARD_INFO_TABLE}.{common_objects.CARD_INDEX_COLUMN} ASC NULLS LAST, {common_objects.SET_INFO_TABLE}.{common_objects.SET_INDEX_COLUMN}, {common_objects.CARD_NAME_COLUMN}"
        elif filter_str == "Card Index Reverse":
            sort_order = f"ORDER BY {common_objects.CARD_INFO_TABLE}.{common_objects.CARD_INDEX_COLUMN} DESC NULLS LAST, {common_objects.SET_INFO_TABLE}.{common_objects.SET_INDEX_COLUMN} DESC, {common_objects.CARD_NAME_COLUMN} DESC"
        elif filter_str == "A-Z":
            sort_order = f"ORDER BY {common_objects.CARD_NAME_COLUMN}"
        elif filter_str == "Z-A":
            sort_order = f"ORDER BY {common_objects.CARD_NAME_COLUMN} DESC"
        elif filter_str == "Have":
            sort_order = f"ORDER BY {common_objects.OWN_COUNT_COLUMN} DESC"
        else:
            sort_order = ""
        return sort_order

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
        params = {common_objects.USER_ID_COLUMN: user_id}
        where_clauses = []
        where_clause = ""
        sort_order = self.get_sort_order(filter_str)

        if set_name:
            where_clauses.append(
                f"{common_objects.SET_NAME_COLUMN}=:{common_objects.SET_NAME_COLUMN}"
            )
            params[common_objects.SET_NAME_COLUMN] = set_name

        if card_name_search_query:
            where_clauses.append(
                f"{common_objects.CARD_NAME_COLUMN} LIKE :card_name_search_query"
            )
            params["card_name_search_query"] = f"%{card_name_search_query}%"

        if filter_ownership:
            if filter_ownership == "have":
                where_clauses.append(f"{common_objects.OWN_COUNT_COLUMN}>0")

        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)
        ID_MOD = f"""
            {common_objects.USER_COLLECTION_TABLE}.{common_objects.ID_COLUMN} AS user_collection_id
            """
        ret_data["set_card_list"] = self.get_data_from_db(
            f"SELECT *, {ID_MOD} {self.BASE_QUERY} {where_clause} {sort_order};",
            params,
        )
        ret_data.update(
            self.get_data_from_db_first_result(
                f"SELECT COUNT({common_objects.OWN_COUNT_COLUMN}) AS count_have {self.BASE_QUERY} {where_clause} {sort_order};",
                params,
            )
        )
        if set_name:
            ret_data[common_objects.SET_NAME_COLUMN] = set_name
            ret_data["count_cards"] = common_objects.get_set_card_count(set_name)
            if ret_data.get("count_have", 0) > 0:
                ret_data["percent_complete"] = round(
                    (ret_data["count_have"] / ret_data["count_cards"]) * 100
                )
            else:
                ret_data["percent_complete"] = 0
        return ret_data

    def get_sets(self):
        return self.get_data_from_db(
            f"SELECT * FROM {common_objects.SET_INFO_TABLE} ORDER BY {common_objects.SET_INDEX_COLUMN} ASC;"
        )

    def get_set_card_count(self, params):
        return self.get_row_item(
            f"SELECT COUNT(*) AS set_card_count FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.SET_ID_COLUMN}=:{common_objects.ID_COLUMN};",
            params,
            "set_card_count",
        )

    def get_null_card_index_count(self, params):
        return self.get_row_item(
            f"SELECT COUNT(CASE WHEN {common_objects.CARD_INDEX_COLUMN} IS NULL THEN 1 ELSE NULL END) AS null_card_index_count FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.SET_ID_COLUMN}=:{common_objects.ID_COLUMN};",
            params,
            "null_card_index_count",
        )

    def get_card_from_id(self, params):
        return self.get_data_from_db_first_result(
            f"SELECT * FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def get_card_info(self, card_id):
        return self.get_data_from_db_first_result(
            f"SELECT * FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.ID_COLUMN}=:{common_objects.CARD_ID_COLUMN};",
            {common_objects.CARD_ID_COLUMN: card_id},
        )

    def get_all_ids(self):
        return self.get_data_from_db(
            f"SELECT {common_objects.TCGP_ID_COLUMN} FROM {common_objects.CARD_INFO_TABLE};"
        )

    def get_card_with_set_index(self, params):
        return self.get_data_from_db_first_result(
            f"SELECT {common_objects.TCGP_ID_COLUMN} FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.SET_ID_COLUMN}=:{common_objects.SET_ID_COLUMN} AND {common_objects.CARD_INDEX_COLUMN}=:{common_objects.CARD_INDEX_COLUMN};",
            params,
        )

    def gifted(self, params):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_GIFT_COLUMN} = 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def set_have(self, params):
        # Update an existing row
        affected_row = self.add_data_to_db(
            f"UPDATE {common_objects.USER_COLLECTION_TABLE} SET {common_objects.OWN_COUNT_COLUMN} = {common_objects.OWN_COUNT_COLUMN} + 1 WHERE {common_objects.CARD_ID_COLUMN}=:{common_objects.CARD_ID_COLUMN} AND {common_objects.USER_ID_COLUMN}=:{common_objects.USER_ID_COLUMN};",
            params,
        )
        # If an existing row doesn't exist, add a new row
        if affected_row is None:
            self.add_data_to_db(
                f"INSERT INTO {common_objects.USER_COLLECTION_TABLE} ({common_objects.USER_ID_COLUMN}, {common_objects.CARD_ID_COLUMN}, {common_objects.OWN_COUNT_COLUMN}) VALUES (:{common_objects.USER_ID_COLUMN}, :{common_objects.CARD_ID_COLUMN}, 1);",
                params,
            )
            params["new"] = True

        # Update the parameters object to include the current own count
        params[common_objects.OWN_COUNT_COLUMN] = self.get_row_item(
            f"SELECT {common_objects.OWN_COUNT_COLUMN} FROM {common_objects.USER_COLLECTION_TABLE} WHERE {common_objects.USER_ID_COLUMN}=:{common_objects.USER_ID_COLUMN} AND {common_objects.CARD_ID_COLUMN}=:{common_objects.CARD_ID_COLUMN};",
            params,
            common_objects.OWN_COUNT_COLUMN,
        )

    def set_want(self, params):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_WANT_COLUMN} = :{common_objects.STATE_WANT_COLUMN} WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def reset_have_want(self):
        return self.get_data_from_db(
            f"DELETE FROM {common_objects.USER_COLLECTION_TABLE};"
        )

    def reset_users(self):
        return self.get_data_from_db(f"DELETE FROM {common_objects.USER_INFO_TABLE};")

    def reset_decks(self):
        self.get_data_from_db(f"DELETE FROM deck_cards;")
        self.get_data_from_db(f"DELETE FROM deck_info;")

    def set_card_index(self, params):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.CARD_INDEX_COLUMN} = :{common_objects.CARD_INDEX_COLUMN} WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def search_card_names(self, params):
        return self.get_data_from_db(
            f"SELECT * FROM card_info WHERE UPPER({common_objects.CARD_NAME_COLUMN}) LIKE UPPER(?);",
            (f"%{params.get(common_objects.CARD_NAME_COLUMN)}%",),
        )

    def generate_random_pack(self, params):
        return self.get_data_from_db(
            f"SELECT * FROM card_info ORDER BY RANDOM() LIMIT :card_count;",
            params,
        )

    def generate_pack_from_set(self, params):
        return self.get_data_from_db(
            f"SELECT * FROM card_info INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN} WHERE {common_objects.SET_INFO_TABLE}.{common_objects.SET_NAME_COLUMN} = :set_name ORDER BY RANDOM() LIMIT :card_count;",
            params,
        )

    def get_user_id(self, params):
        return self.get_row_id(
            f"SELECT {common_objects.ID_COLUMN} FROM {common_objects.USER_INFO_TABLE} WHERE {common_objects.USER_NAME_COLUMN} = :{common_objects.USER_NAME_COLUMN};",
            params,
        )

    def user_login(self, params):
        return self.get_row_id(
            f"SELECT {common_objects.ID_COLUMN} FROM {common_objects.USER_INFO_TABLE} WHERE {common_objects.USER_NAME_COLUMN} = :{common_objects.USER_NAME_COLUMN} AND {common_objects.USER_PASS_COLUMN} = :{common_objects.USER_PASS_COLUMN};",
            params,
        )

    def get_user_hash(self, params):
        return self.get_data_from_db_first_result(
            f"SELECT {common_objects.ID_COLUMN}, {common_objects.USER_PASS_COLUMN} FROM {common_objects.USER_INFO_TABLE} WHERE {common_objects.USER_NAME_COLUMN} = :{common_objects.USER_NAME_COLUMN};",
            params,
        )

    def set_user_pack_time(self, params):
        now = datetime.datetime.now(datetime.UTC)
        iso_string = now.isoformat()
        params[common_objects.LAST_PACK_OPEN_TIME_COLUMN] = iso_string
        return self.add_data_to_db(
            f"UPDATE {common_objects.USER_INFO_TABLE} SET {common_objects.LAST_PACK_OPEN_TIME_COLUMN} = :{common_objects.LAST_PACK_OPEN_TIME_COLUMN} WHERE {common_objects.USER_NAME_COLUMN}=:{common_objects.USER_NAME_COLUMN} AND {common_objects.ID_COLUMN}=:{common_objects.USER_ID_COLUMN};",
            params,
        )

    def get_user_pack_time(self, params):
        return self.get_data_from_db_first_result(
            f"SELECT {common_objects.LAST_PACK_OPEN_TIME_COLUMN} FROM {common_objects.USER_INFO_TABLE} WHERE {common_objects.USER_NAME_COLUMN} = :{common_objects.USER_NAME_COLUMN} AND {common_objects.ID_COLUMN}=:{common_objects.USER_ID_COLUMN};",
            params,
        )

    def set_user_last_set(self, params):
        return self.add_data_to_db(
            f"UPDATE {common_objects.USER_INFO_TABLE} SET {common_objects.LAST_SET_NAME_COLUMN} = :{common_objects.SET_NAME_COLUMN} WHERE {common_objects.USER_NAME_COLUMN}=:{common_objects.USER_NAME_COLUMN} AND {common_objects.ID_COLUMN}=:{common_objects.USER_ID_COLUMN};",
            params,
        )

    def add_card_to_deck(self, user_id, deck_id, card_id):
        """
        Adds a card to the deck. If the card already exists, increments its count.
        """
        query = f"""
            INSERT INTO deck_cards (deck_id, {common_objects.CARD_ID_COLUMN}, card_count)
            SELECT :deck_id, :{common_objects.CARD_ID_COLUMN}, 1
            WHERE EXISTS (
                SELECT 1 FROM deck_info
                WHERE deck_info.id = :deck_id AND deck_info.{common_objects.USER_ID_COLUMN} = :user_id
            )
            ON CONFLICT(deck_id, {common_objects.CARD_ID_COLUMN})
            DO UPDATE SET card_count = card_count + 1
            WHERE EXISTS (
                SELECT 1 FROM deck_info
                WHERE deck_info.id = :deck_id AND deck_info.{common_objects.USER_ID_COLUMN} = :user_id
            );
        """
        self.add_data_to_db(
            query,
            {
                common_objects.USER_ID_COLUMN: user_id,
                "deck_id": deck_id,
                common_objects.CARD_ID_COLUMN: card_id,
            },
        )

    def remove_card_from_deck(self, card_id, deck_id):
        """
        Removes a card from the deck by decrementing its count. If the count reaches 0, the card is removed from the deck.
        """
        params = {
            common_objects.CARD_ID_COLUMN: card_id,
            "deck_id": deck_id,
        }
        # Then, delete the row if card_count is 1
        delete_query = """
            DELETE FROM deck_cards
            WHERE card_id = :card_id AND deck_id = :deck_id AND card_count = 1;
        """
        self.add_data_to_db(
            delete_query,
            params,
        )

        # First, decrement the card_count if it's greater than 1
        update_query = """
            UPDATE deck_cards
            SET card_count = card_count - 1
            WHERE card_id = :card_id AND deck_id = :deck_id AND card_count > 1;
        """
        self.add_data_to_db(update_query, params)

    def create_deck(self, user_id, deck_name, card_list):
        deck_id = self.add_data_to_db(
            f"INSERT INTO deck_info ({common_objects.USER_ID_COLUMN}, deck_name) VALUES (:{common_objects.USER_ID_COLUMN}, :deck_name);",
            {"deck_name": deck_name, "user_id": user_id},
        )
        print(f"New Deck ID: {deck_id}, Deck Name: {deck_name}")
        for card_id in card_list:
            self.add_card_to_deck(user_id, deck_id, card_id)
        return deck_id

    def update_deck(self, deck_name, deck_id, user_id):
        self.add_data_to_db(
            f"UPDATE deck_info SET deck_name = :deck_name WHERE {common_objects.USER_ID_COLUMN}=:{common_objects.USER_ID_COLUMN} AND id=:deck_id;",
            {"deck_name": deck_name, "deck_id": deck_id, "user_id": user_id},
        )

    def get_user_decks(self, user_id):
        return self.get_data_from_db(
            f"SELECT * FROM deck_info WHERE {common_objects.USER_ID_COLUMN} = :{common_objects.USER_ID_COLUMN};",
            {"user_id": user_id},
        )

    def get_deck_cards(self, deck_id, user_id):
        return self.get_data_from_db(
            """
                SELECT card_info.*, deck_cards.card_count
                FROM deck_cards
                JOIN deck_info ON deck_cards.deck_id = deck_info.id
                JOIN card_info ON deck_cards.card_id = card_info.id
                WHERE deck_info.user_id = :user_id AND deck_info.id = :deck_id;
            """,
            {"deck_id": deck_id, "user_id": user_id},
        )

    def get_deck_cards_card_count(self, deck_id, card_id):
        GET_DECK_CARD_COUNT = "SELECT card_count FROM deck_cards WHERE deck_id = :deck_id AND card_id = :card_id;"
        return self.get_row_item(
            GET_DECK_CARD_COUNT, {"deck_id": deck_id, "card_id": card_id}, "card_count"
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
            f"""
                    SELECT
                    SUM(deck_cards.card_count) AS card_count
                    FROM deck_cards
                    JOIN card_info ON deck_cards.card_id = card_info.id
                    WHERE deck_cards.deck_id = :deck_id;
                """,
            {"deck_id": deck_id},
            "card_count",
        )

    def get_deck_info(self, deck_id, user_id):
        return self.get_data_from_db_first_result(
            f"""
                    SELECT * FROM deck_info WHERE id = :deck_id AND user_id = :user_id;
                """,
            {"deck_id": deck_id, "user_id": user_id},
        )

    def get_deck_stats(self, deck_id):
        return {
            "card_count": self.get_deck_card_count(deck_id),
            "card_classes": self.get_deck_card_stat(
                common_objects.CARD_CLASS_COLUMN, deck_id
            ),
            "card_types": self.get_deck_card_stat(
                common_objects.CARD_TYPE_COLUMN, deck_id
            ),
        }
