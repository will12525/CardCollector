import json
import os
import sys
from unittest import TestCase
import math
import random

# import config_file_handler
from database_handler import common_objects
from database_handler.db_getter import DatabaseHandler
from database_handler.db_setter import DBCreator

from image_downloader import download_image

from database_handler.input_file_parser import (
    # load_set_data_dir,
    # load_set_data,
    load_set_list_from_name,
)


# from database_handler.media_metadata_collector import get_playlist_list_index
# import database_handler.db_getter


class TestDBGetterBase(TestCase):
    DB_PATH = "pokemon_card_data.db"
    # DATA_PATH = "../data_files/"
    SET_LIST_PATH = "../data_files/"

    def setUp(self) -> None:
        self.reset_db()
        # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")

        # __init__.patch_get_file_hash(self)
        # __init__.patch_get_ffmpeg_metadata(self)
        # __init__.patch_move_media_file(self)
        # __init__.patch_extract_subclip(self)
        # __init__.patch_update_processed_file(self)

    def erase_db(self):
        if os.path.exists(self.DB_PATH):
            os.remove(self.DB_PATH)

    def populate_db(self):
        with DBCreator() as db_setter_connection:
            db_setter_connection.create_db()
            # index = 0
            # for set_data in load_set_data_dir(self.DATA_PATH):
            #     db_setter_connection.add_set_card_data(set_data)
            #     index += 1
            #     if index == count:
            #         break

    #
    # def populate_specific_set_data(self, set_path):
    #     with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
    #         db_setter_connection.create_db()
    #         db_setter_connection.add_set_card_data(
    #             load_set_data(f"{self.DATA_PATH}{set_path}.html")
    #         )

    def reset_db(self):
        with DatabaseHandler() as db_getter:
            db_getter.reset_have_want()
            db_getter.reset_users()


class TestUserHandling(TestDBGetterBase):
    def test_user_registration(self):
        # self.reset_db()
        self.erase_db()
        self.populate_db()
        db_request_willow = {
            common_objects.USER_NAME_COLUMN: "Willow",
            common_objects.USER_PASS_COLUMN: "12345",
        }
        db_request_leonard = {
            common_objects.USER_NAME_COLUMN: "Leonard",
            common_objects.USER_PASS_COLUMN: "54321",
        }

        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            # db_getter_connection.create_tables()
            # db_getter_connection.reset_users()
            assert db_getter_connection.add_user(db_request_willow)
            assert db_getter_connection.get_user_id(db_request_willow) == 1
            assert not db_getter_connection.add_user(db_request_willow)
            assert db_getter_connection.get_user_id(db_request_willow) == 1
            assert db_getter_connection.add_user(db_request_leonard)
            assert db_getter_connection.get_user_id(db_request_leonard) == 2

    def test_user_login(self):
        # self.reset_db()
        self.erase_db()
        self.populate_db()
        db_request_willow = {
            common_objects.USER_NAME_COLUMN: "Willow",
            common_objects.USER_PASS_COLUMN: "12345",
        }
        db_request_willow_invalid = {
            common_objects.USER_NAME_COLUMN: "Willow",
            common_objects.USER_PASS_COLUMN: "54321",
        }
        db_request_leonard = {
            common_objects.USER_NAME_COLUMN: "Leonard",
            common_objects.USER_PASS_COLUMN: "54321",
        }

        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            # db_getter_connection.create_tables()
            # db_getter_connection.reset_users()
            willow_user_id = db_getter_connection.add_user(db_request_willow)
            leonard_user_id = db_getter_connection.add_user(db_request_leonard)

            assert willow_user_id
            assert leonard_user_id
            assert db_getter_connection.get_user_id(db_request_willow) == willow_user_id
            assert (
                db_getter_connection.get_user_hash(db_request_willow).get(
                    common_objects.USER_PASS_COLUMN
                )
                == db_request_willow[common_objects.USER_PASS_COLUMN]
            )
            assert (
                db_getter_connection.get_user_id(db_request_leonard) == leonard_user_id
            )

            assert db_getter_connection.user_login(db_request_willow) == willow_user_id
            assert (
                db_getter_connection.user_login(db_request_leonard) == leonard_user_id
            )
            assert not db_getter_connection.user_login(db_request_willow_invalid)
            # assert db_getter_connection.get_user_id(db_request_leonard) == 2

            assert db_getter_connection.get_user_id(db_request_willow) == willow_user_id
            assert (
                db_getter_connection.get_user_id(db_request_leonard) == leonard_user_id
            )

    def test_update_user_pack_time(self):
        # self.reset_db()
        self.erase_db()
        self.populate_db()
        db_request_willow = {
            common_objects.USER_NAME_COLUMN: "Willow",
            common_objects.USER_PASS_COLUMN: "12345",
        }

        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            db_request_willow[common_objects.ID_COLUMN] = db_getter_connection.add_user(
                db_request_willow
            )
            db_getter_connection.set_user_pack_time(db_request_willow)


class TestPackGenerator(TestDBGetterBase):
    def test_generate_random_pack(self):
        params = {"card_count": 10}
        with DatabaseHandler() as db_getter:
            pack_of_10_cards = db_getter.generate_random_pack(params)
            for card_info in pack_of_10_cards:
                print(card_info)
        assert len(pack_of_10_cards) == params["card_count"]

    def test_generate_base_set_pack(self):
        params = {"card_count": 10, "set_name": "Base Set (Shadowless)"}
        with DatabaseHandler() as db_getter:
            pack_of_10_cards = db_getter.generate_pack_from_set(params)
            for card_info in pack_of_10_cards:
                print(card_info)
                assert card_info["set_name"] == params["set_name"]
        assert len(pack_of_10_cards) == params["card_count"]

    def test_generate_aquapolis_packs(self):
        params = {"card_count": 10, "set_name": "Aquapolis"}
        with DatabaseHandler() as db_getter:
            pack_of_10_cards = db_getter.generate_pack_from_set(params)
            for card_info in pack_of_10_cards:
                print(card_info)
                assert card_info["set_name"] == params["set_name"]
        assert len(pack_of_10_cards) == params["card_count"]


class TestDBCreatorInit:
    pass


class TestIconCollector(TestDBGetterBase):

    def test_download_card_icons(self):
        destination_path = "../static/card_images"
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            query = db_getter_connection.get_all_ids()

        for index, card_data in enumerate(query):
            download_image(card_data[common_objects.TCGP_ID_COLUMN], destination_path)
            percent_complete = round((index / len(query) * 100), 2)
            print(f"Status: {percent_complete}%")

    # class TestDBCreator(TestDBCreatorInit):
    #
    #     def test_count_alignment_on_read(self):
    #         file_path = f"{self.DATA_PATH}Arceus.html"
    #         set_data = load_set_data(file_path)
    #         # print(set_data)
    #         total_have = 0
    #         total_want = 0
    #         total_cards = 0
    #         cost_have = 0
    #         cost_want = 0
    #         cost_total = 0
    #         set_name = ""
    #         for key, item in set_data.items():
    #             # if item.get("state_want") == 0:
    #             #     continue
    #             print(item)
    #             total_cards += 1
    #             cost_total += item["price"]
    #             set_name = item["set_name"]
    #             if item["state_have"] >= 1:
    #                 total_have += item["state_have"]
    #                 cost_have += item["price"]
    #             if item["state_want"] >= 1:
    #                 total_want += item["state_want"]
    #                 cost_want += item["price"]
    #         print(f"Set name: {set_name}")
    #         print(
    #             f"total_have: {total_have}, total_want: {total_want}, total_cards: {total_cards}, "
    #         )
    #         print(
    #             f"cost_have: {cost_have}, cost_want: {cost_want}, cost_total: {cost_total}, "
    #         )
    #
    #     def test_index_parsing(self):
    #         jungle_file_path = f"{self.DATA_PATH}Jungle.html"
    #         team_rocket_returns_file_path = f"{self.DATA_PATH}Team Rocket Returns.html"
    #         set_data = load_set_data(team_rocket_returns_file_path)
    #         print(json.dumps(set_data, indent=4))
    #
    #     def test_update_index(self):
    #         self.erase_db()
    #         self.populate_specific_set_data("Jungle")
    #         self.populate_specific_set_data("Base Set")
    #         self.populate_specific_set_data("Team Rocket Returns")
    #         # set_data = load_set_data(jungle_file_path)
    #         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
    #             query_base_set = db_getter_connection.query_cards(
    #                 "Base Set (Shadowless)", "", "", "", ""
    #             ).get("set_card_list")
    #             query_jungle = db_getter_connection.query_cards(
    #                 "Jungle", "", "", "", ""
    #             ).get("set_card_list")
    #
    #         print(json.dumps(query_base_set[0], indent=4))
    #         assert query_base_set[0].get(common_objects.CARD_NAME_COLUMN) == "Alakazam"
    #         alakazam_card_id = query_base_set[0].get(common_objects.TCGP_ID_COLUMN)
    #         assert not query_base_set[0].get(common_objects.CARD_INDEX_COLUMN)
    #
    #         print(json.dumps(query_jungle[17], indent=4))
    #         assert query_jungle[17].get(common_objects.CARD_NAME_COLUMN) == "Persian"
    #         persian_card_id = query_jungle[17].get(common_objects.TCGP_ID_COLUMN)
    #         assert not query_jungle[17].get(common_objects.CARD_INDEX_COLUMN)
    #
    #         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
    #             db_getter_connection.set_card_index(
    #                 {
    #                     common_objects.TCGP_ID_COLUMN: alakazam_card_id,
    #                     common_objects.CARD_INDEX_COLUMN: 1,
    #                 }
    #             )
    #             updated_query_base_set = db_getter_connection.query_cards(
    #                 "Base Set (Shadowless)", "", "", "", ""
    #             ).get("set_card_list")
    #
    #             db_getter_connection.set_card_index(
    #                 {
    #                     common_objects.TCGP_ID_COLUMN: persian_card_id,
    #                     common_objects.CARD_INDEX_COLUMN: 7,
    #                 }
    #             )
    #             updated_query_jungle = db_getter_connection.query_cards(
    #                 "Jungle", "", "", "", ""
    #             ).get("set_card_list")
    #
    #         alakazam_card_info = None
    #         for item in updated_query_base_set:
    #             if item.get(common_objects.TCGP_ID_COLUMN) == alakazam_card_id:
    #                 alakazam_card_info = item
    #                 break
    #         print(json.dumps(alakazam_card_info, indent=4))
    #         assert alakazam_card_info.get(common_objects.CARD_INDEX_COLUMN) == 1
    #
    #         persian_card_info = None
    #         for item in updated_query_jungle:
    #             if item.get(common_objects.TCGP_ID_COLUMN) == persian_card_id:
    #                 persian_card_info = item
    #                 break
    #         print(json.dumps(persian_card_info, indent=4))
    #         assert persian_card_info.get(common_objects.CARD_INDEX_COLUMN) == 7
    #
    #     def test_get_all_card_data(self):
    #         self.erase_db()
    #         self.populate_db(1)
    #         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
    #             print(db_getter_connection.get_all_card_data())
    #             # db_setter_connection.create_db()
    #             # for set_data in load_set_data():
    #             #     for card in set_data.values():
    #             #         db_setter_connection.set_card_metadata(card)
    #
    #             # if media_path_data := config_file_handler.load_json_file_content().get("media_folders"):
    #             #     for media_path in media_path_data:
    #             #         # print(media_path)
    #             #         db_setter_connection.setup_media_directory(media_path)
    #
    def test_get_all_set_card_data(self):
        with DatabaseHandler() as db_getter_connection:
            card_list = db_getter_connection.get_all_set_card_data(
                {common_objects.SET_NAME_COLUMN: "Aquapolis"}
            )
            assert len(card_list) == 186
            card_list = db_getter_connection.get_all_set_card_data(
                {common_objects.SET_NAME_COLUMN: "Arceus"}
            )
            print(len(card_list))
            assert len(card_list) == 111

    def test_search_card_names(self):
        with DatabaseHandler() as db_getter_connection:
            card_list = db_getter_connection.search_card_names(
                {common_objects.CARD_NAME_COLUMN: "Aipom"}
            )
        assert len(card_list) == 16
        for card in card_list:
            assert card.get(common_objects.CARD_NAME_COLUMN) == "Aipom"

    #
    def test_get_sets(self):
        with DatabaseHandler() as db_getter_connection:
            set_list = db_getter_connection.get_sets()

        # -1 because missing data files for base set 2
        assert len(set_list) == common_objects.get_set_count() - 1

    def test_query_base_set_user_collection_complete(self):
        set_name = "Base Set (Shadowless)"
        user_id = 1
        self.reset_db()
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            db_getter_connection.add_user({common_objects.USER_NAME_COLUMN: "Willow"})
            for card in db_getter_connection.get_all_set_card_data(
                {
                    common_objects.SET_NAME_COLUMN: set_name,
                    common_objects.USER_ID_COLUMN: user_id,
                }
            ):
                db_getter_connection.set_have(
                    {
                        common_objects.OWN_COUNT_COLUMN: 1,
                        common_objects.CARD_ID_COLUMN: card.get(
                            common_objects.ID_COLUMN
                        ),
                        common_objects.USER_ID_COLUMN: user_id,
                    }
                )
            query_base_set = db_getter_connection.query_collection(
                set_name, "Sets", "", "", "", user_id
            )

        print(query_base_set.keys())
        print(query_base_set)
        print(query_base_set.get("count_have"))
        assert query_base_set.get("count_have") == common_objects.get_set_card_count(
            set_name
        )
        assert query_base_set.get("percent_complete") == 100
        assert len(
            query_base_set.get("set_card_list")
        ) == common_objects.get_set_card_count(set_name)
        for card in query_base_set.get("set_card_list"):
            assert card.get(common_objects.SET_NAME_COLUMN) == set_name
            assert card.get(common_objects.USER_ID_COLUMN) == user_id
            assert card.get(common_objects.OWN_COUNT_COLUMN) == 1

    def test_query_base_set_user_collection_increment(self):
        set_name = "Base Set (Shadowless)"
        user_id = 1
        set_request = {
            common_objects.SET_NAME_COLUMN: set_name,
            common_objects.USER_ID_COLUMN: user_id,
        }
        card_increment_data = {
            common_objects.OWN_COUNT_COLUMN: 0,
            common_objects.CARD_ID_COLUMN: None,
            common_objects.USER_ID_COLUMN: user_id,
        }
        user_info = {
            common_objects.USER_NAME_COLUMN: "Willow",
            common_objects.USER_PASS_COLUMN: "12345",
        }
        self.reset_db()
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            db_getter_connection.add_user(user_info)
            base_set_card_list = db_getter_connection.get_all_set_card_data(set_request)
            # print(base_set_card_list[0])
            card_increment_data[common_objects.CARD_ID_COLUMN] = base_set_card_list[
                0
            ].get(common_objects.ID_COLUMN)
            for i in range(10):
                print(card_increment_data)
                db_getter_connection.set_have(card_increment_data)
                base_set_card_list = db_getter_connection.get_all_set_card_data(
                    set_request
                )
                first_card = base_set_card_list[0]
                assert first_card[common_objects.OWN_COUNT_COLUMN] == (i + 1)
                assert (
                    first_card[common_objects.ID_COLUMN]
                    == card_increment_data[common_objects.CARD_ID_COLUMN]
                )
                assert card_increment_data[common_objects.OWN_COUNT_COLUMN] == (i + 1)

    def test_query_base_set_user_collection_half(self):
        set_name = "Base Set (Shadowless)"
        user_id = 1
        self.reset_db()
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            db_getter_connection.add_user({common_objects.USER_NAME_COLUMN: "Willow"})
            base_set_card_list = db_getter_connection.get_all_set_card_data(
                {
                    common_objects.SET_NAME_COLUMN: set_name,
                    common_objects.USER_ID_COLUMN: user_id,
                }
            )
            half_length = math.ceil(
                len(base_set_card_list) / 2
            )  # Calculate the approximate midpoint
            selected_items = random.sample(base_set_card_list, half_length)

            for card in selected_items:
                db_getter_connection.set_have(
                    {
                        common_objects.OWN_COUNT_COLUMN: 1,
                        common_objects.CARD_ID_COLUMN: card.get(
                            common_objects.ID_COLUMN
                        ),
                        common_objects.USER_ID_COLUMN: user_id,
                    }
                )
            query_base_set = db_getter_connection.query_collection(
                set_name, "Sets", "", "", "", user_id
            )

        print(query_base_set.keys())
        print(query_base_set)
        print(query_base_set.get("count_have"))
        assert (
            query_base_set.get("count_have")
            == common_objects.get_set_card_count(set_name) / 2
        )
        assert query_base_set.get("percent_complete") == 50
        assert len(
            query_base_set.get("set_card_list")
        ) == common_objects.get_set_card_count(set_name)
        for card in query_base_set.get("set_card_list"):
            assert card.get(common_objects.SET_NAME_COLUMN) == set_name
            if card.get(common_objects.OWN_COUNT_COLUMN):
                assert card.get(common_objects.USER_ID_COLUMN) == user_id
                assert card.get(common_objects.OWN_COUNT_COLUMN) == 1
            else:
                assert not card.get(common_objects.USER_ID_COLUMN)
                assert not card.get(common_objects.OWN_COUNT_COLUMN)

    def test_query_filters(self):
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            query_arceus_alpha_ascending = db_getter_connection.query_collection(
                "Arceus", "A-Z", "", "", "", None
            )
            query_arceus_alpha_descending = db_getter_connection.query_collection(
                "Arceus", "Z-A", "", "", "", None
            )
            query_arceus_index_ascending = db_getter_connection.query_collection(
                "Arceus", "Card Index", "", "", "", None
            )
            query_arceus_index_descending = db_getter_connection.query_collection(
                "Arceus", "Card Index Reverse", "", "", "", None
            )

        assert len(query_arceus_alpha_ascending.get("set_card_list")) == 111
        last_card_name = ""
        for query in query_arceus_alpha_ascending.get("set_card_list"):
            # print(query)
            assert query["set_name"] == "Arceus"
            assert query["card_name"] >= last_card_name
            last_card_name = query["card_name"]

        assert len(query_arceus_alpha_descending.get("set_card_list")) == 111
        last_card_name = ""
        for query in query_arceus_alpha_descending.get("set_card_list"):
            if not last_card_name:
                last_card_name = query["card_name"]
                continue
            assert query["set_name"] == "Arceus"
            assert query["card_name"] <= last_card_name
            last_card_name = query["card_name"]

        print(query_arceus_index_ascending.get("set_card_list"))
        assert len(query_arceus_index_ascending.get("set_card_list")) == 111
        last_card_index = 0
        for query in query_arceus_index_ascending.get("set_card_list"):
            # print(query)
            if not query["card_index"]:
                continue
            assert query["set_name"] == "Arceus"
            assert query["card_index"] >= last_card_index
            last_card_index = query["card_index"]

        print(query_arceus_index_descending.get("set_card_list"))
        assert len(query_arceus_index_descending.get("set_card_list")) == 111
        last_card_index = 0
        for query in query_arceus_index_descending.get("set_card_list"):
            # print(query)
            if not last_card_index:
                last_card_index = query["card_index"]
                continue
            if not query["card_index"]:
                continue
            assert query["set_name"] == "Arceus"
            assert query["card_index"] <= last_card_index
            last_card_index = query["card_index"]

    #     def test_chilling_reign(self):
    #         self.erase_db()
    #         self.populate_specific_set_data("SWSH06 Chilling Reign")
    #
    #     def test_call_of_legends(self):
    #         self.erase_db()
    #         self.populate_specific_set_data("Call of Legends")
    #
    #     def test_alphabetical(self):
    #         self.erase_db()
    #         self.populate_specific_set_data("Jungle")
    #         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
    #             query_jungle = db_getter_connection.query_cards(
    #                 "Jungle", "A-Z", "", "", ""
    #             ).get("set_card_list")
    #         # print(json.dumps(query_jungle, indent=4))
    #         assert len(query_jungle) == 64
    #         last_card_name = ""
    #         for query in query_jungle:
    #             print(query)
    #             assert query["set_name"] == "Jungle"
    #             assert query["card_name"] >= last_card_name
    #             last_card_name = query["card_name"]
    #
    #     def test_for_gaps_in_card_index(self):
    #         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
    #             set_list = db_getter_connection.get_sets()
    #             for set_item in set_list:
    #                 set_name = set_item.get(common_objects.SET_NAME_COLUMN)
    #                 last_card_index = 0
    #                 for card in db_getter_connection.query_cards(
    #                     set_name, "Sets", "", "", ""
    #                 ).get("set_card_list"):
    #                     current_card_index = card.get(common_objects.CARD_INDEX_COLUMN)
    #                     if current_card_index:
    #                         if (
    #                             last_card_index + 1
    #                         ) != current_card_index and current_card_index != 999:
    #                             print(
    #                                 f"GAP!: last_card_index: {last_card_index}, current_card_index: {current_card_index}, current_card_name: {card.get(common_objects.CARD_NAME_COLUMN)}, set_name: {set_name}"
    #                             )
    #                         last_card_index = card.get(common_objects.CARD_INDEX_COLUMN)
    #
    def test_get_all_null_indexed_cards(self):
        input_required = 0
        with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
            set_list = db_getter_connection.get_sets()
            for set_item in set_list:
                set_name = set_item.get(common_objects.SET_NAME_COLUMN)
                set_card_list = load_set_list_from_name(self.SET_LIST_PATH, set_name)
                print(set_name, json.dumps(set_card_list, indent=4))
                for card in db_getter_connection.query_collection(
                    set_name, "Sets", "", "", "", None
                ).get("set_card_list"):
                    if not card.get(common_objects.CARD_INDEX_COLUMN):
                        print(json.dumps(card, indent=4))
                        print(
                            "https://www.tcgplayer.com/product/"
                            + str(card["tcgp_id"])
                            + "/pokmeon-"
                            + card["tcgp_path"]
                        )
                        found_card_matches = set_card_list.get_all_cards_matching_name(
                            card.get(common_objects.CARD_NAME_COLUMN)
                        )
                        filtered_card_matches = []
                        for card_match in found_card_matches:
                            if not db_getter_connection.get_card_with_set_index(
                                {
                                    common_objects.CARD_INDEX_COLUMN: card_match.get(
                                        common_objects.CARD_INDEX_COLUMN
                                    ),
                                    common_objects.SET_ID_COLUMN: set_item.get(
                                        common_objects.ID_COLUMN
                                    ),
                                }
                            ):
                                filtered_card_matches.append(card_match)

                        if len(filtered_card_matches) == 1:
                            new_card_index = filtered_card_matches[0].get(
                                common_objects.CARD_INDEX_COLUMN
                            )
                            # provided_index = input(f"Confirm: {new_card_index}")
                            # if provided_index == "":
                            print(f"Applying found index: {new_card_index}")
                            card[common_objects.CARD_INDEX_COLUMN] = new_card_index
                            print(card)
                            # print(type(new_card_index))
                            db_getter_connection.set_card_index(card)
                            # elif provided_index == "n":
                            #     pass
                            # else:
                            #     print(f"Applying provided index: {provided_index}")
                            #     card[common_objects.CARD_INDEX_COLUMN] = provided_index
                            #     print(card)
                            #     db_getter_connection.set_card_index(card)
                        else:
                            print(
                                "\n".join([str(card) for card in filtered_card_matches])
                            )
                            # provided_index = int(
                            #     input("Provide index: ").replace("\n", "").strip()
                            # )
                            input_required += 1
                            provided_index = 1
                            if provided_index:
                                print(f"Applying provided index: {provided_index}")
                                # print(type(provided_index))
                                card[common_objects.CARD_INDEX_COLUMN] = provided_index
                                print(card)
                                db_getter_connection.set_card_index(card)
                        # input("wait...")
        print("input_required: ", input_required)


#
#     def test_get_all_set_counts(self):
#         sum_unindexed = 0
#         sum_missing = 0
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             set_list = db_getter_connection.get_sets()
#             for set_item in set_list:
#                 set_name = set_item.get(common_objects.SET_NAME_COLUMN)
#                 set_card_count = db_getter_connection.get_set_card_count(set_item)
#                 expected_set_card_count = common_objects.get_set_card_count(set_name)
#                 null_card_index_count = db_getter_connection.get_null_card_index_count(
#                     set_item
#                 )
#                 sum_unindexed += null_card_index_count
#                 sum_missing += expected_set_card_count - set_card_count
#                 print(
#                     f"Diff: {expected_set_card_count - set_card_count}, Expected: {expected_set_card_count}, Actual: {set_card_count}, Unindexed: {null_card_index_count}, Set: {set_item.get(common_objects.SET_NAME_COLUMN)}",
#                 )
#                 # print(set_item)
#             # query_jungle = db_getter_connection.query_cards(
#             #     "Jungle", "A-Z", "", ""
#             # ).get("set_card_list")
#         print(f"Sum missing: {sum_missing}, Sum unindexed: {sum_unindexed}")
#
#     def test_get_queries_sums(self):
#         self.erase_db()
#         self.populate_db(1)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             query = db_getter_connection.query_cards(
#                 "", "Price: Low - High", "", "", ""
#             )
#             query_want = db_getter_connection.query_cards(
#                 "", "Price: Low - High", "", "want", ""
#             )
#             query_have = db_getter_connection.query_cards(
#                 "", "Price: Low - High", "", "have", ""
#             )
#         print(json.dumps(query_want, indent=4))
#         print(json.dumps(query_have, indent=4))
#
#         assert query["count_want"] == 160
#         assert query["count_have"] == 29
#         assert query["sum_price"] == 7172.389999999993
#
#     def test_update_have_want(self):
#         self.erase_db()
#         self.populate_db(1)
#         card_id_dict = {common_objects.TCGP_ID_COLUMN: 83487}
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             base_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert base_query[common_objects.STATE_WANT_COLUMN] == 1
#             assert base_query[common_objects.STATE_HAVE_COLUMN] == 0
#             assert base_query[common_objects.STATE_GIFT_COLUMN] == 0
#             db_getter_connection.increase_want(card_id_dict)
#             card_data_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert card_data_query[common_objects.STATE_WANT_COLUMN] == 2
#             db_getter_connection.decrease_want(card_id_dict)
#             db_getter_connection.decrease_want(card_id_dict)
#             card_data_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert card_data_query[common_objects.STATE_WANT_COLUMN] == 0
#             db_getter_connection.increase_have(card_id_dict)
#             db_getter_connection.increase_have(card_id_dict)
#             card_data_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert card_data_query[common_objects.STATE_HAVE_COLUMN] == 2
#             db_getter_connection.decrease_have(card_id_dict)
#             card_data_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert card_data_query[common_objects.STATE_HAVE_COLUMN] == 1
#             db_getter_connection.gifted(card_id_dict)
#             card_data_query = db_getter_connection.get_card_from_id(card_id_dict)
#             assert card_data_query[common_objects.STATE_GIFT_COLUMN] == 1
#
#         print(json.dumps(base_query, indent=4))
#
#         assert base_query[common_objects.CARD_NAME_COLUMN] == "Aipom"
#         assert base_query[common_objects.STATE_HAVE_COLUMN] == 0
#         assert base_query[common_objects.STATE_WANT_COLUMN] == 1
#
#     def test_download_card_icons(self):
#         # self.erase_db()
#         # with DBCreator(co.DBType.PHYSICAL) as db_connection:
#         #     db_connection.create_db()
#         #     for set_data in load_set_data_dir(self.DATA_PATH):
#         #         db_connection.add_set_card_data(set_data)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             # query = db_getter_connection.query_cards("", "", "", "")
#             query = db_getter_connection.get_all_ids()
#             # query_want = db_getter_connection.query_cards("", "", "", "want")
#             # query_have = db_getter_connection.query_cards("", "", "", "have")
#         # print(json.dumps(query, indent=4))
#         id_list = [card_data[common_objects.TCGP_ID_COLUMN] for card_data in query]
#         # print(len(id_list))
#         download_tcgp_card_images(id_list)
#
#     def test_get_query_all(self):
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             # query = db_getter_connection.query_cards("", "", "", "")
#             query = db_getter_connection.get_all_ids()
#             # query = db_getter_connection.get_test()
#             # query_want = db_getter_connection.query_cards("", "", "", "want")
#             # query_have = db_getter_connection.query_cards("", "", "", "have")
#         # print(json.dumps(query, indent=4))
#         id_list = [card_data[common_objects.TCGP_ID_COLUMN] for card_data in query]
#         print(len(id_list))
#         # print(json.dumps(query_have, indent=4))
#
#         # print(query["count_have"])
#         # print(query["count_want"])
#         # print(query["price_want"])
#         # print(query["price_have"])
#         # print(query["sum_price"])
#         # print(query["count_cards"])
#         # print(query["percent_complete"])
#
#         # assert query["count_want"] == 160
#         # assert query["count_have"] == 29
#         # assert query["sum_price"] == 7172.389999999993
