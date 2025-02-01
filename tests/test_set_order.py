import json
from unittest import TestCase
import set_order
import re

from bs4 import BeautifulSoup as bs


class Test(TestCase):
    def test_get_set_name_list(self):
        for set_name in set_order.get_set_name_list():
            assert type(set_name) is str

    def test_get_set_name_size(self):
        assert len(set_order.set_info) == set_order.get_set_count()

    def test_get_set_location_by_name(self):
        set_name_list = set_order.get_set_name_list()
        for index, set_name in enumerate(set_name_list):
            assert index == set_order.get_set_index_by_name(set_name)

    def test_get_set_name_by_index(self):
        for index in range(0, set_order.get_set_count()):
            assert set_order.set_info[index]["name"] == set_order.get_set_name_by_index(
                index
            )
