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

sql_create_card_info_table = f"""{CREATE_TABLE} {common_objects.CARD_INFO_TABLE} (
                                    {common_objects.STATE_HAVE_COLUMN} integer NOT NULL,
                                    {common_objects.STATE_WANT_COLUMN} integer NOT NULL,
                                    {common_objects.CARD_NAME_COLUMN} TEXT NOT NULL COLLATE NOCASE,
                                    {common_objects.SET_ID_COLUMN} integer NOT NULL,
                                    {common_objects.PRICE_COLUMN} integer NOT NULL,
                                    {common_objects.CARD_RARITY_COLUMN} text DEFAULT "",
                                    {common_objects.CARD_INDEX_COLUMN} integer,
                                    {common_objects.STATE_GIFT_COLUMN} integer DEFAULT 0,
                                    {common_objects.TCGP_ID_COLUMN} integer NOT NULL PRIMARY KEY,
                                    {common_objects.TCGP_PATH_COLUMN} text NOT NULL,
                                    FOREIGN KEY ({common_objects.SET_ID_COLUMN}) REFERENCES {common_objects.SET_INFO_TABLE} ({common_objects.ID_COLUMN})
                                );"""

sql_insert_card_info_table = f"INSERT INTO {common_objects.CARD_INFO_TABLE} VALUES(:{common_objects.STATE_HAVE_COLUMN}, :{common_objects.STATE_WANT_COLUMN}, :{common_objects.CARD_NAME_COLUMN}, :{common_objects.SET_ID_COLUMN}, :{common_objects.PRICE_COLUMN}, :{common_objects.CARD_RARITY_COLUMN}, :{common_objects.CARD_INDEX_COLUMN}, :{common_objects.STATE_GIFT_COLUMN}, :{common_objects.TCGP_ID_COLUMN}, :{common_objects.TCGP_PATH_COLUMN});"

sql_create_set_info_table = f"""{CREATE_TABLE} {common_objects.SET_INFO_TABLE} (
                                    {common_objects.ID_COLUMN} integer PRIMARY KEY,
                                    {common_objects.SET_NAME_COLUMN} TEXT NOT NULL UNIQUE COLLATE NOCASE,
                                    {common_objects.SET_INDEX_COLUMN} integer UNIQUE
                                );"""

sql_insert_set_info_table = f"{INSERT_IGNORE} {common_objects.SET_INFO_TABLE} VALUES(:{common_objects.ID_COLUMN}, :{common_objects.SET_NAME_COLUMN}, :{common_objects.SET_INDEX_COLUMN});"


class DBCreator(DBConnection):

    def create_db(self):
        if self.VERSION != self.check_db_version():
            # Run db update procedure
            pass
        db_table_creation_script = "".join(
            ["BEGIN;", sql_create_set_info_table, sql_create_card_info_table, "COMMIT;"]
        )
        self.create_tables(db_table_creation_script)

    def set_card_metadata(self, card_data) -> int:
        return self.add_data_to_db(sql_insert_card_info_table, card_data)

    def add_set_card_data(self, set_data):
        set_id = None
        for card in set_data.values():
            if not set_id:
                set_dict = common_objects.default_set_dict.copy()
                set_dict[common_objects.SET_NAME_COLUMN] = card.get(
                    common_objects.SET_NAME_COLUMN
                )
                set_dict[common_objects.SET_INDEX_COLUMN] = card.get(
                    common_objects.SET_INDEX_COLUMN
                )
                card[common_objects.SET_ID_COLUMN] = self.set_set_data(set_dict)
                if not card[common_objects.SET_ID_COLUMN]:
                    card[common_objects.SET_ID_COLUMN] = self.get_set_id_from_name(
                        card.get(common_objects.SET_NAME_COLUMN)
                    )
                set_id = card[common_objects.SET_ID_COLUMN]
            else:
                card[common_objects.SET_ID_COLUMN] = set_id
            self.set_card_metadata(card)

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

    # def set_media_directory_info(self, media_directory_info) -> int:
    #     defaulted_media_directory_info = (
    #         common_objects.default_media_directory_info.copy()
    #     )
    #     defaulted_media_directory_info.update(media_directory_info)
    #     return self.add_data_to_db(
    #         sql_insert_media_folder_path_table, defaulted_media_directory_info
    #     )
    #
    # def get_media_directory_info(self, item_id) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_MEDIA_DIRECTORY_INFO, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_all_media_directory_info(self):
    #     return self.get_data_from_db(GET_ALL_MEDIA_DIRECTORIES)
    #
    # def set_playlist_metadata(self, playlist_metadata) -> int:
    #     return self.add_data_to_db(SET_PLAYLIST_METADATA, playlist_metadata)
    #
    # def get_playlist_metadata(self, item_id: int) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_PLAYLIST_METADATA, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_playlist_id_from_title(self, playlist_metadata) -> int:
    #     return self.get_row_id(GET_PLAYLIST_ID_FROM_TITLE, playlist_metadata)
    #
    # def set_tv_show_metadata(self, tv_show_metadata) -> int:
    #     return self.add_data_to_db(SET_TV_SHOW_METADATA, tv_show_metadata)
    #
    # def get_tv_show_metadata(self, item_id) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_TV_SHOW_METADATA, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_tv_show_id_from_playlist_id(self, tv_show_metadata) -> int:
    #     return self.get_row_id(GET_TV_SHOW_ID_FROM_PLAYLIST_ID, tv_show_metadata)
    #
    # def set_season_metadata(self, season_metadata) -> int:
    #     return self.add_data_to_db(sql_insert_season_info_table, season_metadata)
    #
    # def get_season_metadata(self, item_id) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_SEASON_METADATA, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_season_id_from_tv_show_id_season_index(self, season_metadata) -> int:
    #     return self.get_row_id(
    #         GET_SEASON_ID_FROM_TV_SHOW_ID_SEASON_INDEX, season_metadata
    #     )
    #
    # def set_media_metadata(self, media_metadata) -> int:
    #     return self.add_data_to_db(sql_insert_media_info_table, media_metadata)
    #
    # def get_media_metadata(self, item_id) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_MEDIA_METADATA, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_media_id_from_media_title_path(self, media_metadata) -> int:
    #     return self.get_row_id(GET_MEDIA_ID_FROM_TITLE_PATH, media_metadata)
    #
    # def get_media_metadata_from_media_folder_path_id(
    #     self, media_metadata
    # ) -> list[dict]:
    #     return self.get_data_from_db(
    #         GET_MEDIA_METADATA_FROM_MEDIA_FOLDER_PATH_ID, media_metadata
    #     )
    #
    # def add_media_to_playlist(self, media_metadata) -> int:
    #     return self.add_data_to_db(sql_insert_playlist_media_list_table, media_metadata)
    #
    # def get_playlist_entry(self, item_id) -> dict:
    #     return self.get_data_from_db_first_result(
    #         GET_PLAYLIST_LIST_METADATA, {common_objects.ID_COLUMN: item_id}
    #     )
    #
    # def get_playlist_id_from_playlist_media_metadata(self, media_metadata) -> int:
    #     return self.get_row_id(GET_PLAYLIST_ID_FROM_PLAYLIST_MEDIA_INFO, media_metadata)
