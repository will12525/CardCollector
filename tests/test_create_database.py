import json
import os
from unittest import TestCase

# import config_file_handler
from database_handler import common_objects
from database_handler.db_getter import DatabaseHandler
from database_handler.db_setter import (
    DBCreator,
    sql_create_card_info_table,
    sql_insert_card_info_table,
)
from database_handler.input_file_parser import (
    load_set_data_dir,
    load_set_list_from_name,
    # get_all_cards_matching_name,
)


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

    def erase_db(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

    def populate_db(self, count):
        pass
        # with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
        #     db_setter_connection.create_db()
        #     index = 0
        #     for set_data in load_set_data_dir(self.DATA_PATH):
        #         db_setter_connection.add_set_card_data(set_data)
        #         index += 1
        #         if index == count:
        #             break


class TestDBCreator(TestDBCreatorInit):

    def test_fill_database(self):
        # pass
        self.erase_db()
        with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
            db_setter_connection.create_db()
            for set_data in load_set_data_dir(self.DATA_PATH):
                db_setter_connection.add_set_card_data(set_data)

    def test_add_users(self):
        # pass
        self.erase_db()
        with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
            db_setter_connection.create_db()
            db_setter_connection.add_user(
                {
                    common_objects.USER_NAME_COLUMN: "Willow",
                    common_objects.USER_PASS_COLUMN: "1234",
                }
            )
            db_setter_connection.add_user(
                {
                    common_objects.USER_NAME_COLUMN: "Tori",
                    common_objects.USER_PASS_COLUMN: "1234",
                }
            )
            db_setter_connection.add_user(
                {
                    common_objects.USER_NAME_COLUMN: "Leonard",
                    common_objects.USER_PASS_COLUMN: "1234",
                }
            )

    def test_custom_injection(self):
        card_machamp = {
            common_objects.OWN_COUNT_COLUMN: 0,
            common_objects.STATE_WANT_COLUMN: 0,
            common_objects.CARD_NAME_COLUMN: "Machamp",
            common_objects.SET_ID_COLUMN: 0,
            common_objects.PRICE_COLUMN: 6.0,
            common_objects.CARD_RARITY_COLUMN: "Unlimited Holofoil",
            common_objects.CARD_INDEX_COLUMN: 8,
            common_objects.STATE_GIFT_COLUMN: 0,
            common_objects.TCGP_ID_COLUMN: 107004,
            common_objects.TCGP_PATH_COLUMN: "deck-exclusives-machamp",
            common_objects.SET_NAME_COLUMN: "Base Set (Shadowless)",
            common_objects.SET_INDEX_COLUMN: 0,
        }
        card_treecko = {
            common_objects.OWN_COUNT_COLUMN: 0,
            common_objects.STATE_WANT_COLUMN: 0,
            common_objects.CARD_NAME_COLUMN: "Treecko Star",
            common_objects.SET_ID_COLUMN: 0,
            common_objects.PRICE_COLUMN: 500.0,
            common_objects.CARD_RARITY_COLUMN: "Holofoil",
            common_objects.CARD_INDEX_COLUMN: 109,
            common_objects.STATE_GIFT_COLUMN: 0,
            common_objects.TCGP_ID_COLUMN: 90046,
            common_objects.TCGP_PATH_COLUMN: "team-rocket-returns-treecko-star",
            common_objects.SET_NAME_COLUMN: "Team Rocket Returns",
            common_objects.SET_INDEX_COLUMN: 0,
        }
        card_vaporeon = {
            common_objects.OWN_COUNT_COLUMN: 0,
            common_objects.STATE_WANT_COLUMN: 0,
            common_objects.CARD_NAME_COLUMN: "Vaporeon Star",
            common_objects.SET_ID_COLUMN: 0,
            common_objects.PRICE_COLUMN: 450.0,
            common_objects.CARD_RARITY_COLUMN: "Holofoil",
            common_objects.CARD_INDEX_COLUMN: 102,
            common_objects.STATE_GIFT_COLUMN: 0,
            common_objects.TCGP_ID_COLUMN: 90292,
            common_objects.TCGP_PATH_COLUMN: "power-keepers-vaporeon-star",
            common_objects.SET_NAME_COLUMN: "Power Keepers",
            common_objects.SET_INDEX_COLUMN: 0,
        }
        with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
            db_setter_connection.insert_card(card_machamp)
            db_setter_connection.insert_card(card_treecko)
            db_setter_connection.insert_card(card_vaporeon)

        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            print(db_getter_connection.get_card_from_id(card_machamp))
            print(db_getter_connection.get_card_from_id(card_treecko))
            print(db_getter_connection.get_card_from_id(card_vaporeon))

    def test_setup_new_media_metadata(self):
        self.erase_db()
        self.populate_db(1)
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            card_data_list = db_getter_connection.get_all_card_data()
        assert type(card_data_list) is list
        print(len(card_data_list))
        assert len(card_data_list) == 186
        for card_data in card_data_list:
            print(card_data)
            assert type(card_data) is dict
            assert len(card_data) == 12

        # if media_path_data := config_file_handler.load_json_file_content().get("media_folders"):
        #     for media_path in media_path_data:
        #         # print(media_path)
        #         db_setter_connection.setup_media_directory(media_path)

    def test_get_all_sets(self):
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            set_list = db_getter_connection.get_sets()
            print(set_list)

    def test_add_set_data(self):
        self.erase_db()
        base_set_set = {
            common_objects.ID_COLUMN: None,
            common_objects.SET_NAME_COLUMN: "Base set",
            common_objects.SET_INDEX_COLUMN: common_objects.get_set_index("Base set"),
        }
        aquapolis_set = {
            common_objects.ID_COLUMN: None,
            common_objects.SET_NAME_COLUMN: "Aquapolis",
            common_objects.SET_INDEX_COLUMN: common_objects.get_set_index("Aquapolis"),
        }
        with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
            db_setter_connection.create_db()
            assert 1 == db_setter_connection.set_set_data(base_set_set)
            assert not db_setter_connection.set_set_data(base_set_set)
            assert 2 == db_setter_connection.set_set_data(aquapolis_set)
            print(
                db_setter_connection.get_set_id_from_name(
                    base_set_set.get(common_objects.SET_NAME_COLUMN)
                )
            )
            assert 1 == db_setter_connection.get_set_id_from_name(
                base_set_set.get(common_objects.SET_NAME_COLUMN, {})
            )
            assert 2 == db_setter_connection.get_set_id_from_name(
                aquapolis_set.get(common_objects.SET_NAME_COLUMN, {})
            )

        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            set_list = db_getter_connection.get_sets()
        print(set_list)
        assert len(set_list) == 2
        assert set_list[0].get(common_objects.SET_NAME_COLUMN) == base_set_set.get(
            common_objects.SET_NAME_COLUMN
        )
        assert set_list[1].get(common_objects.SET_NAME_COLUMN) == aquapolis_set.get(
            common_objects.SET_NAME_COLUMN
        )

    def test_multiple_set_names(self):
        expected_result = [
            {"id": 1, "set_name": "Aquapolis", common_objects.SET_INDEX_COLUMN: 14},
            {"id": 2, "set_name": "Arceus", common_objects.SET_INDEX_COLUMN: 42},
        ]
        self.erase_db()
        self.populate_db(2)
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            set_list = db_getter_connection.get_sets()
        assert expected_result == set_list

    def test_table_constructors(self):
        # 0 == False
        # 1 == True
        print(sql_insert_card_info_table)
        print(sql_create_card_info_table)

    def test_same_db(self):
        SET_PATH = "../data_files/"
        SET_LIST_PATH = "../data_files/"
        cards_missing_index = 0
        cards_missing_rarity = 0
        cards_missing_type = 0
        cards_missing_class = 0
        card_count = 0
        rarity_names = {}
        # pedia_cache = {}
        #
        # for set_name in common_objects.get_set_name_list():
        #     pedia_cache[set_name] = load_set_list_from_name(SET_LIST_PATH, set_name)
        #
        # assert len(pedia_cache) == common_objects.get_set_count()

        set_data_list = list(load_set_data_dir(SET_PATH))

        print(len(set_data_list))
        assert len(set_data_list) == 106

        self.erase_db()

        # with DatabaseHandler(
        #     file_name="pokemon_card_data_backup.db"
        # ) as db_backup_handler:
        # db_backup_handler.set_card_index(
        #     {
        #         common_objects.TCGP_ID_COLUMN: 83510,
        #         common_objects.CARD_INDEX_COLUMN: 2,
        #     }
        # )
        for set_data in set_data_list:
            assert common_objects.get_set_index(set_data.set_name)
            card_count += len(set_data.card_dict)
            print(set_data.to_dict())
            # print(set_data)
            for tcgp_id, card_data in set_data.card_dict.items():
                # set_name = card_data.card_set.set_name
                # backup_card_data = db_backup_handler.get_card_from_id(
                #     {common_objects.TCGP_ID_COLUMN: tcgp_id}
                # )

                # print(
                #     json.dumps(card_data.to_dict(), indent=4),
                #     json.dumps(backup_card_data, indent=4),
                # )
                if rarity_names.get(card_data.rarity):
                    rarity_names[card_data.rarity] += 1
                else:
                    rarity_names[card_data.rarity] = 1

                if not card_data.card_index:
                    cards_missing_index += 1
                if not card_data.card_type:
                    cards_missing_type += 1
                if not card_data.card_class:
                    cards_missing_class += 1
                if not card_data.rarity:
                    cards_missing_rarity += 1
                    # input(json.dumps(card_data.to_dict(), indent=4))

                # assert card_data.card_name == backup_card_data["card_name"]
                # assert card_data.tcgp_path == backup_card_data["tcgp_path"]
                # if card_data.card_index:
                #     assert card_data.card_index == backup_card_data["card_index"]
                # else:
                #     print(
                #         "Missing Index",
                #         card_data.to_dict(),
                #         backup_card_data,
                #     )

        # Original required 2802 user input
        # New requires 3196 user input
        print(
            "card_count: ",
            card_count,
            "Expected:",
            common_objects.get_total_card_count(),
        )
        print("cards_missing_index: ", cards_missing_index)
        print("cards_missing_type: ", cards_missing_type)
        print("cards_missing_class: ", cards_missing_class)
        print("cards_missing_rarity: ", cards_missing_rarity)
        assert 15032 <= card_count <= common_objects.get_total_card_count()
        assert cards_missing_rarity <= 1572
        assert cards_missing_index <= 2608
        assert cards_missing_type <= 4565
        assert cards_missing_class <= 2735

        print(json.dumps(rarity_names, indent=4))

        with DBCreator() as db_setter_connection:
            db_setter_connection.create_db()
            for set_data in set_data_list:
                db_setter_connection.add_set_card_data(set_data)
