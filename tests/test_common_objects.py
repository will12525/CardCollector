from unittest import TestCase
import database_handler.common_objects as co


class TestCardInfo(TestCase):
    def test_constructor(self):
        card_info = co.CardInfo()
        print(vars(card_info))

    def test_get_set_index(self):
        assert 1 == co.get_set_index("Base Set (Shadowless)")

    def test_get_set_name_from_index(self):
        assert "Base Set (Shadowless)" == co.get_set_name_from_index(1)

    def test_check_energy_card(self):
        assert co.check_energy_card("Grass Energy")

    def test_get_total_card_count(self):
        assert co.get_total_card_count() == 15077
