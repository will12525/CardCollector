import json
from . import common_objects
from .db_access import DBConnection


"""

SETS
ID | SET_NAME | CARD_COUNT | RELEASE_DATE |  

CARDS
ID | SET_ID | RARITY_ID | TYPE_ID | SET_INDEX | CARD_NAME | OWN | PRESENT | COST | 

RARITY 
ID | RARITY | 

TYPE
ID | TYPE

"""


INSERT_IGNORE = "INSERT OR IGNORE INTO"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS"

# f"UPDATE card_info SET card_type = 1 WHERE {common_objects.TCGP_ID_COLUMN}=:{common_objects.TCGP_ID_COLUMN};"

sql_create_card_info_table = f"""{CREATE_TABLE} {common_objects.CARD_INFO_TABLE} (
                                    {common_objects.ID_COLUMN} integer PRIMARY KEY AUTOINCREMENT,
                                    {common_objects.CARD_NAME_COLUMN} TEXT NOT NULL COLLATE NOCASE,
                                    {common_objects.SET_ID_COLUMN} integer NOT NULL,
                                    {common_objects.CARD_TYPE_COLUMN} text DEFAULT "",
                                    {common_objects.CARD_RARITY_COLUMN} text DEFAULT "",
                                    {common_objects.CARD_INDEX_COLUMN} integer,
                                    {common_objects.TCGP_ID_COLUMN} integer NOT NULL UNIQUE,
                                    {common_objects.TCGP_PATH_COLUMN} text NOT NULL,
                                    {common_objects.CARD_CLASS_COLUMN} text NOT NULL,
                                    {common_objects.CARD_ATTACK_COLUMN} TEXT DEFAULT '',
                                    {common_objects.CARD_ENERGY_COST_COLUMN} TEXT DEFAULT '',
                                    {common_objects.CARD_TEXT_COLUMN} TEXT DEFAULT '',
                                    FOREIGN KEY ({common_objects.SET_ID_COLUMN}) REFERENCES {common_objects.SET_INFO_TABLE} ({common_objects.ID_COLUMN})
                                );"""

sql_insert_card_info_table = f"INSERT INTO {common_objects.CARD_INFO_TABLE} ({common_objects.CARD_NAME_COLUMN}, {common_objects.SET_ID_COLUMN}, {common_objects.CARD_TYPE_COLUMN}, {common_objects.CARD_RARITY_COLUMN}, {common_objects.CARD_INDEX_COLUMN}, {common_objects.TCGP_ID_COLUMN}, {common_objects.TCGP_PATH_COLUMN}, {common_objects.CARD_CLASS_COLUMN}) VALUES (:{common_objects.CARD_NAME_COLUMN}, :{common_objects.SET_ID_COLUMN}, :{common_objects.CARD_TYPE_COLUMN}, :{common_objects.CARD_RARITY_COLUMN}, :{common_objects.CARD_INDEX_COLUMN}, :{common_objects.TCGP_ID_COLUMN}, :{common_objects.TCGP_PATH_COLUMN}, :{common_objects.CARD_CLASS_COLUMN});"

sql_create_set_info_table = f"""{CREATE_TABLE} {common_objects.SET_INFO_TABLE} (
                                    {common_objects.ID_COLUMN} integer PRIMARY KEY AUTOINCREMENT,
                                    {common_objects.SET_NAME_COLUMN} TEXT NOT NULL UNIQUE COLLATE NOCASE,
                                    {common_objects.SET_INDEX_COLUMN} integer UNIQUE,
                                    {common_objects.SET_CARD_COUNT_COLUMN} integer NOT NULL
                                );"""

sql_insert_set_info_table = f"{INSERT_IGNORE} {common_objects.SET_INFO_TABLE} ({common_objects.SET_NAME_COLUMN}, {common_objects.SET_INDEX_COLUMN}, {common_objects.SET_CARD_COUNT_COLUMN}) VALUES (:{common_objects.SET_NAME_COLUMN}, :{common_objects.SET_INDEX_COLUMN}, :{common_objects.SET_CARD_COUNT_COLUMN});"

sql_create_user_info_table = f"""{CREATE_TABLE} {common_objects.USER_INFO_TABLE} (
                                    {common_objects.ID_COLUMN} integer PRIMARY KEY AUTOINCREMENT,
                                    {common_objects.USER_NAME_COLUMN} TEXT NOT NULL UNIQUE,
                                    {common_objects.USER_PASS_COLUMN} TEXT NOT NULL,
                                    {common_objects.LAST_PACK_OPEN_TIME_COLUMN} TEXT DEFAULT "",
                                    {common_objects.LAST_SET_NAME_COLUMN} TEXT DEFAULT "",
                                    {common_objects.LAST_DECK_ID_COLUMN} integer
                                );"""


sql_create_user_collection_table = f"""{CREATE_TABLE} {common_objects.USER_COLLECTION_TABLE} (
                                    {common_objects.ID_COLUMN} integer PRIMARY KEY AUTOINCREMENT,
                                    {common_objects.USER_ID_COLUMN} integer NOT NULL,
                                    {common_objects.CARD_ID_COLUMN} integer NOT NULL,
                                    {common_objects.OWN_COUNT_COLUMN} integer NOT NULL,
                                    FOREIGN KEY ({common_objects.USER_ID_COLUMN}) REFERENCES {common_objects.USER_INFO_TABLE} ({common_objects.ID_COLUMN}),
                                    FOREIGN KEY ({common_objects.CARD_ID_COLUMN}) REFERENCES {common_objects.CARD_INFO_TABLE} ({common_objects.ID_COLUMN})
                                    UNIQUE ({common_objects.USER_ID_COLUMN}, {common_objects.CARD_ID_COLUMN})
                                );"""

sql_insert_user_collection_table = f"{INSERT_IGNORE} {common_objects.USER_COLLECTION_TABLE} ({common_objects.USER_ID_COLUMN}, {common_objects.CARD_ID_COLUMN}, {common_objects.OWN_COUNT_COLUMN}) VALUES (:{common_objects.USER_ID_COLUMN}, :{common_objects.CARD_ID_COLUMN}, :{common_objects.OWN_COUNT_COLUMN});"

sql_create_deck_info_table = f"""
                {CREATE_TABLE} deck_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    deck_name TEXT DEFAULT "",
                    FOREIGN KEY (user_id) REFERENCES user_info (id)
                );
            """
sql_create_deck_cards_info_table = f"""
                {CREATE_TABLE} deck_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER NOT NULL,
                    card_id INTEGER NOT NULL,
                    card_count INTEGER NOT NULL,
                    FOREIGN KEY (deck_id) REFERENCES deck_info (id),
                    FOREIGN KEY (card_id) REFERENCES card_info (id),
                    UNIQUE (deck_id, card_id)
                );
            """
sql_create_ban_info_table = f"""
                {CREATE_TABLE} ban_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL UNIQUE,
                    ban_reason TEXT DEFAULT '',
                    FOREIGN KEY (card_id) REFERENCES card_info (id)
                );
            """


class DBCreator(DBConnection):

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
                sql_create_set_info_table,
                sql_create_card_info_table,
                sql_create_user_info_table,
                sql_create_user_collection_table,
                sql_create_deck_info_table,
                sql_create_deck_cards_info_table,
                sql_create_ban_info_table,
            ]
            self.execute_db_script(db_table_creation_script)

    def set_card_metadata(self, card_data) -> int:
        return self.add_data_to_db(sql_insert_card_info_table, card_data)

    def add_set_card_data(self, set_data):
        set_data.set_id = self.set_set_data(set_data.to_dict())

        for card in set_data.card_dict.values():
            card.set_id = set_data.set_id
            self.set_card_metadata(card.to_dict())

    def insert_card(self, card):
        card[common_objects.SET_ID_COLUMN] = self.get_set_id_from_name(
            card.get(common_objects.SET_NAME_COLUMN)
        )
        print(card)
        self.set_card_metadata(card)

    def set_set_data(self, set_data):
        return self.add_data_to_db(sql_insert_set_info_table, set_data)

    def get_set_id_from_name(self, set_name) -> dict:
        return self.get_row_id(
            f"SELECT {common_objects.ID_COLUMN} FROM {common_objects.SET_INFO_TABLE} WHERE {common_objects.SET_NAME_COLUMN}=:{common_objects.SET_NAME_COLUMN};",
            {common_objects.SET_NAME_COLUMN: set_name},
        )

    def update_database(self, current_version):
        """Updates the database schema to the latest version."""
        if current_version == 1:
            current_version = 2
            print(f"Updating database to version {current_version}...")
            query_list = [
                sql_create_deck_info_table,
                sql_create_deck_cards_info_table,
                sql_create_ban_info_table,
                f"ALTER TABLE {common_objects.CARD_INFO_TABLE} ADD COLUMN {common_objects.CARD_ATTACK_COLUMN} TEXT DEFAULT '';",
                f"ALTER TABLE {common_objects.CARD_INFO_TABLE} ADD COLUMN {common_objects.CARD_ENERGY_COST_COLUMN} TEXT DEFAULT '';",
                f"ALTER TABLE {common_objects.CARD_INFO_TABLE} ADD COLUMN {common_objects.CARD_TEXT_COLUMN} TEXT DEFAULT '';",
                f"ALTER TABLE {common_objects.USER_INFO_TABLE} ADD COLUMN {common_objects.LAST_SET_NAME_COLUMN} TEXT DEFAULT '';"
                f"ALTER TABLE {common_objects.USER_INFO_TABLE} ADD COLUMN {common_objects.LAST_DECK_ID_COLUMN} INTEGER;"
                f"UPDATE version_info SET version = {current_version} WHERE id = 1;",
            ]
            self.execute_db_script(query_list)
            print(f"Database updated to version {current_version}.")
