import json
import os
from unittest import TestCase

# import config_file_handler
import flask_endpoints
from database_handler.db_getter import DatabaseHandler


class TestDBCreatorInit(TestCase):
    DB_PATH = "pokemon_card_data.db"
    DATA_PATH = "../data_files/"

    def setUp(self) -> None:
        pass
        # if os.path.exists(self.DB_PATH):
        #     os.remove(self.DB_PATH)
        # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")

        # __init__.patch_get_file_hash(self)
        # __init__.patch_get_ffmpeg_metadata(self)
        # __init__.patch_move_media_file(self)
        # __init__.patch_extract_subclip(self)
        # __init__.patch_update_processed_file(self)

    # def erase_db(self):
    #     if os.path.exists(self.DB_PATH):
    #         os.remove(self.DB_PATH)
    #
    # def populate_db(self, count):
    #     pass
    # with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
    #     db_setter_connection.create_db()
    #     index = 0
    #     for set_data in load_set_data_dir(self.DATA_PATH):
    #         db_setter_connection.add_set_card_data(set_data)
    #         index += 1
    #         if index == count:
    #             break


class TestDBCreator(TestDBCreatorInit):

    def test_can_user_add_card_to_deck(self):
        # pass
        with DatabaseHandler() as db_getter_connection:
            flask_endpoints.can_user_add_card_to_deck(db_getter_connection, 1, 1, 1)
