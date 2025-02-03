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
        card_set_search_query,
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

        if card_set_search_query:
            where_clauses.append(
                f"{common_objects.SET_INFO_TABLE}.{common_objects.SET_NAME_COLUMN} LIKE :card_season_search_query"
            )
            params["card_season_search_query"] = f"%{card_set_search_query}%"

        if filter_ownership:
            if filter_ownership == "have":
                where_clauses.append(f"{common_objects.OWN_COUNT_COLUMN}>0")
            elif filter_ownership == "want":
                where_clauses.append(f"{common_objects.STATE_WANT_COLUMN}>0")
            else:
                pass

        if where_clauses:
            where_clause = "WHERE " + " AND ".join(where_clauses)

        ret_data["set_card_list"] = self.get_data_from_db(
            f"SELECT * {self.BASE_QUERY} {where_clause} {sort_order};",
            params,
        )
        ret_data.update(
            self.get_data_from_db_first_result(
                f"SELECT COUNT({common_objects.OWN_COUNT_COLUMN}) AS count_have {self.BASE_QUERY} {where_clause} {sort_order};",
                params,
            )
        )

        if set_name:
            ret_data["count_cards"] = common_objects.get_set_card_count(set_name)
            if ret_data.get("count_have", 0) > 0:
                ret_data["percent_complete"] = round(
                    (ret_data["count_have"] / ret_data["count_cards"]) * 100
                )
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

    def get_all_ids(self):
        return self.get_data_from_db(
            f"SELECT {common_objects.TCGP_ID_COLUMN} FROM {common_objects.CARD_INFO_TABLE};"
        )

    def get_card_with_set_index(self, params):
        return self.get_data_from_db_first_result(
            f"SELECT {common_objects.TCGP_ID_COLUMN} FROM {common_objects.CARD_INFO_TABLE} WHERE {common_objects.SET_ID_COLUMN}=:{common_objects.SET_ID_COLUMN} AND {common_objects.CARD_INDEX_COLUMN}=:{common_objects.CARD_INDEX_COLUMN};",
            params,
        )

    def increase_want(self, params):
        pass
        # return self.get_data_from_db(
        #     f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_WANT_COLUMN} = {common_objects.STATE_WANT_COLUMN} + 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
        #     params,
        # )

    def decrease_want(self, params):
        pass
        # return self.get_data_from_db(
        #     f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_WANT_COLUMN} = {common_objects.STATE_WANT_COLUMN} - 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
        #     params,
        # )

    def increase_have(self, params):
        pass
        # return self.get_data_from_db(
        #     f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_HAVE_COLUMN} = {common_objects.STATE_HAVE_COLUMN} + 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
        #     params,
        # )

    def decrease_have(self, params):
        pass
        # return self.get_data_from_db(
        #     f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_HAVE_COLUMN} = {common_objects.STATE_HAVE_COLUMN} - 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
        #     params,
        # )

    def gifted(self, params):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_GIFT_COLUMN} = 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def set_have(self, params):
        affected_row = self.add_data_to_db(
            f"UPDATE {common_objects.USER_COLLECTION_TABLE} SET {common_objects.OWN_COUNT_COLUMN} = {common_objects.OWN_COUNT_COLUMN} + 1 WHERE {common_objects.CARD_ID_COLUMN}=:{common_objects.CARD_ID_COLUMN} AND {common_objects.USER_ID_COLUMN}=:{common_objects.USER_ID_COLUMN};",
            params,
        )
        if not affected_row:
            self.add_data_to_db(
                f"INSERT INTO {common_objects.USER_COLLECTION_TABLE} VALUES (null, :{common_objects.USER_ID_COLUMN}, :{common_objects.CARD_ID_COLUMN}, :{common_objects.OWN_COUNT_COLUMN});",
                params,
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
