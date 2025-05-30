# File: tests/test_unit_common_objects.py

import pytest
from app.utils.common_objects import get_set_card_count, tcgp_set_info


def test_get_set_card_count_valid_set():
    set_name = "Base Set (Shadowless)"
    expected_count = tcgp_set_info[set_name]["card_count"]
    assert get_set_card_count(set_name) == expected_count


def test_get_set_card_count_invalid_set():
    set_name = "Nonexistent Set"
    assert get_set_card_count(set_name) is None
