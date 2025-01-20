import json
import os
import sys
from unittest import TestCase

# import config_file_handler
from database_handler import common_objects
from database_handler.db_getter import DatabaseHandler
from database_handler.db_setter import DBCreator

from image_downloader import download_image

# from database_handler.input_file_parser import (
#     load_set_data_dir,
#     load_set_data,
#     download_tcgp_card_images,
#     get_pedia_set_data,
#     get_all_cards_matching_name,
# )


# from database_handler.media_metadata_collector import get_playlist_list_index
# import database_handler.db_getter


class TestDBGetterBase(TestCase):
    DB_PATH = "pokemon_card_data.db"
    # DATA_PATH = "../data_files/set_htmls/"
    # SET_LIST_PATH = "../data_files/set_list_htmls/"

    def setUp(self) -> None:
        self.reset_db()
        # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")

        # __init__.patch_get_file_hash(self)
        # __init__.patch_get_ffmpeg_metadata(self)
        # __init__.patch_move_media_file(self)
        # __init__.patch_extract_subclip(self)
        # __init__.patch_update_processed_file(self)

    # def erase_db(self):
    #     if os.path.exists(self.DB_PATH):
    #         os.remove(self.DB_PATH)

    # def populate_db(self, count):
    #     with DBCreator(common_objects.DBType.PHYSICAL) as db_setter_connection:
    #         db_setter_connection.create_db()
    #         index = 0
    #         for set_data in load_set_data_dir(self.DATA_PATH):
    #             db_setter_connection.add_set_card_data(set_data)
    #             index += 1
    #             if index == count:
    #                 break
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
#     def test_get_all_set_card_data(self):
#         self.erase_db()
#         self.populate_db(2)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             card_list = db_getter_connection.get_all_set_card_data(
#                 {common_objects.SET_NAME_COLUMN: "Aquapolis"}
#             )
#             assert len(card_list) == 186
#             card_list = db_getter_connection.get_all_set_card_data(
#                 {common_objects.SET_NAME_COLUMN: "Arceus"}
#             )
#             print(len(card_list))
#             assert len(card_list) == 111
#
#     def test_search_card_names(self):
#         self.erase_db()
#         self.populate_db(1)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             card_list = db_getter_connection.search_card_names(
#                 {common_objects.CARD_NAME_COLUMN: "Ai"}
#             )
#             print(card_list)
#         assert len(card_list) == 3
#         assert card_list[0].get(common_objects.CARD_NAME_COLUMN) == "Aipom"
#         assert card_list[1].get(common_objects.CARD_NAME_COLUMN) == "Rainbow Energy"
#         assert card_list[2].get(common_objects.CARD_NAME_COLUMN) == "Remoraid"
#
#     def test_get_sets(self):
#         self.erase_db()
#         self.populate_db(2)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             print(db_getter_connection.get_sets())
#
#     def test_get_queries(self):
#         self.erase_db()
#         self.populate_db(2)
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             query_aquapolis = db_getter_connection.query_cards(
#                 "Aquapolis", "Price: Low - High", "", "", ""
#             ).get("set_card_list")
#             query_arceus = db_getter_connection.query_cards(
#                 "Arceus", "A-Z", "", "", ""
#             ).get("set_card_list")
#             query_card_names = db_getter_connection.query_cards(
#                 "", "Price: Low - High", "ai", "", ""
#             ).get("set_card_list")
#             query_aquapolis_card_names = db_getter_connection.query_cards(
#                 "Aquapolis", "Price: High - Low", "ai", "", ""
#             ).get("set_card_list")
#             query_all_price_high = db_getter_connection.query_cards(
#                 "", "Price: High - Low", "", "", ""
#             ).get("set_card_list")
#         # print(len(query_aquapolis))
#         # print(len(query_arceus))
#
#         assert len(query_aquapolis) == 186
#         last_price = 0
#         for query in query_aquapolis:
#             # print(query)
#             assert query["set_name"] == "Aquapolis"
#             assert query["price"] >= last_price
#             last_price = query["price"]
#
#         assert len(query_arceus) == 111
#         last_card_name = ""
#         for query in query_arceus:
#             # print(query)
#             assert query["set_name"] == "Arceus"
#             assert query["card_name"] > last_card_name
#             last_card_name = query["card_name"]
#
#         assert len(query_all_price_high) == 297
#         last_price = sys.float_info.max
#         for query in query_all_price_high:
#             assert query["price"] <= last_price
#             last_price = query["price"]
#
#         assert len(query_card_names) == 4
#         last_price = 0
#         for query in query_card_names:
#             # print(query)
#             assert "ai" in query["card_name"].lower()
#             assert query["price"] >= last_price
#             last_price = query["price"]
#
#         assert len(query_aquapolis_card_names) == 3
#         last_price = sys.float_info.max
#         for query in query_aquapolis_card_names:
#             print(query)
#             assert "ai" in query["card_name"].lower()
#             assert query["price"] <= last_price
#             last_price = query["price"]
#
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
#     def test_get_all_null_indexed_cards(self):
#         with DatabaseHandler(common_objects.DBType.PHYSICAL) as db_getter_connection:
#             set_list = db_getter_connection.get_sets()
#             for set_item in set_list:
#                 set_name = set_item.get(common_objects.SET_NAME_COLUMN)
#                 set_card_list = get_pedia_set_data(
#                     f"{self.SET_LIST_PATH}{set_name}.html"
#                 )
#                 print(set_name, json.dumps(set_card_list, indent=4))
#                 for card in db_getter_connection.query_cards(
#                     set_name, "Sets", "", "", ""
#                 ).get("set_card_list"):
#                     if not card.get(common_objects.CARD_INDEX_COLUMN):
#                         print(json.dumps(card, indent=4))
#                         print(
#                             "https://www.tcgplayer.com/product/"
#                             + str(card["tcgp_id"])
#                             + "/pokmeon-"
#                             + card["tcgp_path"]
#                         )
#                         found_card_matches = get_all_cards_matching_name(
#                             card.get(common_objects.CARD_NAME_COLUMN), set_card_list
#                         )
#                         filtered_card_matches = []
#                         for card_match in found_card_matches:
#                             if not db_getter_connection.get_card_with_set_index(
#                                 {
#                                     common_objects.CARD_INDEX_COLUMN: card_match.get(
#                                         common_objects.CARD_INDEX_COLUMN
#                                     ),
#                                     common_objects.SET_ID_COLUMN: set_item.get(
#                                         common_objects.ID_COLUMN
#                                     ),
#                                 }
#                             ):
#                                 filtered_card_matches.append(card_match)
#
#                         if len(filtered_card_matches) == 1:
#                             new_card_index = filtered_card_matches[0].get(
#                                 common_objects.CARD_INDEX_COLUMN
#                             )
#                             # provided_index = input(f"Confirm: {new_card_index}")
#                             # if provided_index == "":
#                             print(f"Applying found index: {new_card_index}")
#                             card[common_objects.CARD_INDEX_COLUMN] = new_card_index
#                             print(card)
#                             # print(type(new_card_index))
#                             db_getter_connection.set_card_index(card)
#                             # elif provided_index == "n":
#                             #     pass
#                             # else:
#                             #     print(f"Applying provided index: {provided_index}")
#                             #     card[common_objects.CARD_INDEX_COLUMN] = provided_index
#                             #     print(card)
#                             #     db_getter_connection.set_card_index(card)
#                         else:
#                             print(
#                                 "\n".join([str(card) for card in filtered_card_matches])
#                             )
#                             provided_index = int(
#                                 input("Provide index: ").replace("\n", "").strip()
#                             )
#                             if provided_index:
#                                 print(f"Applying provided index: {provided_index}")
#                                 # print(type(provided_index))
#                                 card[common_objects.CARD_INDEX_COLUMN] = provided_index
#                                 print(card)
#                                 db_getter_connection.set_card_index(card)
#                         # input("wait...")
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
