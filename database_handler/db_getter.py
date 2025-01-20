import json
import pathlib

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
        print(params)
        return self.get_data_from_db(
            f"SELECT * FROM {common_objects.CARD_INFO_TABLE} INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN} WHERE {common_objects.SET_NAME_COLUMN}=:{common_objects.SET_NAME_COLUMN};",
            params,
        )

    SORT_ALPHABETICAL = "GLOB '[A-Za-z]*'"

    BASE_QUERY = f"FROM {common_objects.CARD_INFO_TABLE} INNER JOIN {common_objects.SET_INFO_TABLE} ON {common_objects.CARD_INFO_TABLE}.{common_objects.SET_ID_COLUMN} = {common_objects.SET_INFO_TABLE}.{common_objects.ID_COLUMN}"
    STAT_QUERY_SELECT = " ".join(
        [
            f"SELECT",
            f"SUM({common_objects.STATE_HAVE_COLUMN}) AS count_have,",
            f"SUM({common_objects.STATE_WANT_COLUMN}) AS count_want,",
            f"ROUND(SUM(CASE WHEN {common_objects.STATE_WANT_COLUMN} > 0 THEN {common_objects.PRICE_COLUMN} ELSE 0 END), 2) AS price_want,",
            f"ROUND(SUM(CASE WHEN {common_objects.STATE_HAVE_COLUMN} > 0 THEN {common_objects.PRICE_COLUMN} ELSE 0 END), 2) AS price_have,",
            f"ROUND(SUM({common_objects.PRICE_COLUMN}), 2) AS sum_price,",
            f"COUNT(1) AS count_cards",
        ]
    )

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
        elif filter_str == "Price: Low - High":
            sort_order = f"ORDER BY {common_objects.PRICE_COLUMN}"
        elif filter_str == "Price: High - Low":
            sort_order = f"ORDER BY {common_objects.PRICE_COLUMN} DESC"
        elif filter_str == "Have":
            sort_order = f"ORDER BY {common_objects.STATE_HAVE_COLUMN} DESC"
        elif filter_str == "Want":
            sort_order = f"ORDER BY {common_objects.STATE_WANT_COLUMN} DESC"
        else:
            sort_order = ""
        return sort_order

    def query_cards(
        self,
        set_name,
        filter_str,
        card_name_search_query,
        filter_ownership,
        card_set_search_query,
    ):
        ret_data = {}
        params = {}
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
                where_clauses.append(f"{common_objects.STATE_HAVE_COLUMN}>0")
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
                f"{self.STAT_QUERY_SELECT} {self.BASE_QUERY} {where_clause} {sort_order};",
                params,
            )
        )
        if ret_data["count_cards"] > 0:
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
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_HAVE_COLUMN} = :{common_objects.STATE_HAVE_COLUMN} WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def set_want(self, params):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_WANT_COLUMN} = :{common_objects.STATE_WANT_COLUMN} WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};",
            params,
        )

    def reset_have_want(self):
        return self.get_data_from_db(
            f"UPDATE {common_objects.CARD_INFO_TABLE} SET {common_objects.STATE_WANT_COLUMN} = 0, {common_objects.STATE_HAVE_COLUMN} = 0;"
        )

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
