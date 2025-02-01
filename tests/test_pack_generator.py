import json
from unittest import TestCase

from database_handler.db_getter import DatabaseHandler
from pack_generator import Pack
from database_handler import common_objects


class TestPack(TestCase):
    def test_open(self):
        with DatabaseHandler() as db_getter_connection:
            json_request = {"set_name": "Base Set (Shadowless)", "user_id": 1}
            # Generate the pack
            set_card_list = db_getter_connection.get_all_set_card_data(json_request)
        # print(json.dumps(set_card_list, indent=4))

        pack = Pack(set_card_list)
        pulled_cards = pack.open()
        for card in pulled_cards:
            print(card)
        assert len(pulled_cards) == 10

    def test_generate_many_packs(self):
        with DatabaseHandler() as db_getter_connection:
            json_request = {"set_name": "Base Set (Shadowless)", "user_id": 1}
            set_card_list = db_getter_connection.get_all_set_card_data(json_request)
        for i in range(100):
            pack = Pack(set_card_list)
            pulled_cards = pack.open()
            assert len(pulled_cards) == 10
            assert None not in pulled_cards

    def test_generate_pack_from_every_set(self):
        for set_name in common_objects.get_set_name_list():
            with DatabaseHandler() as db_getter_connection:
                json_request = {"set_name": set_name, "user_id": 1}
                set_card_list = db_getter_connection.get_all_set_card_data(json_request)
            if set_card_list:
                print(set_card_list)
                for i in range(100):
                    pack = Pack(set_card_list)
                    pulled_cards = pack.open()
                    assert len(pulled_cards) == 10
                    # assert None not in pulled_cards
                    # for card in pulled_cards:
                    #     assert card.get("card_name")
            else:
                assert set_name == "Base set 2"
