import os
import pathlib

import requests
from bs4 import BeautifulSoup
import re
from deck import read_file
from . import common_objects


def extract_string(input_str: str):
    input_str = input_str.strip()
    input_str = input_str.replace("\u00e2\u2122\u201a", " M")
    input_str = input_str.replace("\u00c3\u00a9", "e")
    input_str = input_str.replace("\u00e2\u2122\u20ac", " F")
    input_str = input_str.replace("\u00ce\u00b1", "Alpha")
    input_str = input_str.replace("\u00ce\u00b2", "Beta")
    input_str = input_str.replace("\u00ce\u00b3", "Gamma")
    input_str = input_str.replace("\u00ce\u00b4", "Delta")
    input_str = input_str.replace("\n        ", " ")
    input_str = input_str.replace("\n", " ")
    input_str = input_str.replace("\u00e2\u02dc\u2020", "star")
    input_str = input_str.replace("\u00a0", " ")
    # if str("\\") in input_str:
    #     print(input_str)
    return input_str


def extract_card_index(card_index_str):
    card_index_division_regex = r"(\d+)/\d+"
    if card_index_search := re.search(card_index_division_regex, card_index_str):
        return int(card_index_search.groups()[0])
    elif card_index_search := re.search(r"H(\d+)/H\d+", card_index_str):
        return int(card_index_search.groups()[0])
    elif card_index_search := re.search(r"RC(\d+)/RC\d+", card_index_str):
        return int(card_index_search.groups()[0])
    elif card_index_search := re.search(r"TG(\d+)/TG\d+", card_index_str):
        return int(card_index_search.groups()[0])
    elif card_index_search := re.search(r"(\d+)a/\d+", card_index_str):
        return int(card_index_search.groups()[0])
    elif card_index_search := re.search(r"(\d+)b/\d+", card_index_str):
        return int(card_index_search.groups()[0])
    elif "ONE" == card_index_str:
        return 1
    elif "TWO" == card_index_str:
        return 2
    elif "THREE" == card_index_str:
        return 3
    elif "FOUR" == card_index_str:
        return 4
    else:
        print("Error occurred")
        return card_index_str


def extract_card_type(card_type_str):
    if re.search(r"T \[St]", card_type_str):
        return "Stadium"
    elif re.search(r"T \[TM]", card_type_str):
        return "Trainer"
    elif re.search(r"T \[Su]", card_type_str):
        return "Support"
    elif re.search(r"T \[PT]", card_type_str):
        return "Trainer"
    elif re.search(r"T\n", card_type_str):
        return "Trainer"
    elif re.search(r"Su\n", card_type_str):
        return "Support"
    elif re.search(r"St\n", card_type_str):
        return "Stadium"

    return None


class PediaCardData:
    card_name = ""
    card_type = ""
    card_rarity = ""
    card_index = None

    def __init__(self, table_row_cells):
        # print(table_row_cells)
        # row_dict[common_objects.CARD_INDEX_COLUMN] = cells[0].text.strip()
        self.card_name = extract_string(table_row_cells[2].text)

        card_type_a = table_row_cells[3].find("a")
        if card_type_a and card_type_a.has_attr("title"):
            self.card_type = str(card_type_a.get("title"))
        else:
            type_text = extract_card_type(table_row_cells[3].text)
            if type_text:
                self.card_type = type_text
            # else:
            #     print("Break")

        card_rarity_a = table_row_cells[4].find("a")
        if card_rarity_a and card_rarity_a.has_attr("title"):
            self.card_rarity = extract_string(card_rarity_a.get("title"))

        self.card_index = extract_card_index(table_row_cells[0].text.strip())
        # if (
        #     not self.card_index
        #     or not self.card_name
        #     or not self.card_type
        #     or not self.card_rarity
        # ):
        #     print("Break")

    def to_dict(self):
        if self.card_type:
            return {
                "card_name": self.card_name,
                "card_type": self.card_type,
                "card_rarity": self.card_rarity,
                "card_index": self.card_index,
            }
        return {
            "card_name": self.card_name,
            "card_rarity": self.card_rarity,
            "card_index": self.card_index,
        }


def extract_set_list_htmls(html_soup):
    table_data = []
    first_index_header = True
    table = html_soup.find("tbody")

    # Check if table exists
    if table:
        # Extract headers and table data
        for row in table.find_all("tr"):
            if first_index_header:
                # print(row)
                first_index_header = False
                continue

            cells = row.find_all(["td", "th"])
            if cells and len(cells) == 6:
                table_data.append(PediaCardData(cells).to_dict())
    return table_data


class CardData:
    have = 0
    want = 0
    card_name = ""
    price = 0
    rarity = ""
    card_index = None
    tcgp_id = None
    tcgp_path = ""
    card_set = None

    def __init__(self, table_row):
        pass


def card_name_cleanup(row_dict):
    card_rarity_regex = r"- \[(.+)\]$"
    card_index_division_regex = r"- (\d+)/\d+"
    card_index_regex = r" \((\d+)\)"
    if card_rarity_search := re.search(
        card_rarity_regex, row_dict[common_objects.CARD_NAME_COLUMN]
    ):
        # row_dict[common_objects.CARD_RARITY_COLUMN] = card_rarity_search.groups()[
        #     -1
        # ]
        row_dict[common_objects.CARD_NAME_COLUMN] = row_dict[
            common_objects.CARD_NAME_COLUMN
        ][: card_rarity_search.span()[0]].strip()

    if card_index_search := re.search(
        card_index_division_regex, row_dict[common_objects.CARD_NAME_COLUMN]
    ):
        row_dict[common_objects.CARD_INDEX_COLUMN] = int(card_index_search.groups()[0])
        row_dict[common_objects.CARD_NAME_COLUMN] = row_dict[
            common_objects.CARD_NAME_COLUMN
        ][: card_index_search.span()[0]].strip()
    if card_index_search := re.search(
        card_index_regex, row_dict[common_objects.CARD_NAME_COLUMN]
    ):
        row_dict[common_objects.CARD_INDEX_COLUMN] = int(card_index_search.groups()[0])
        row_dict[common_objects.CARD_NAME_COLUMN] = row_dict[
            common_objects.CARD_NAME_COLUMN
        ][: card_index_search.span()[0]].strip()


def extract_set_htmls(html_soup):
    """Fetches the webpage, parses the HTML, and extracts data from the first table.

    Returns:
        A list of dictionaries, where each dictionary represents a row (tr) containing data from the first table (td elements).
        An empty list is returned if no table is found.
    """
    table_data = {}
    table = html_soup.find("tbody")

    set_name = ""

    # Check if table exists
    if not table:
        return table_data

    # track_card_name = "Dugtrio"

    # Extract headers and table data
    for row in table.find_all("tr"):
        # track_card = False
        cells = row.find_all(["td", "th"])
        # Extract data for each cell based on headers

        row_dict = common_objects.default_card_dict.copy()
        row_dict["cost"] = float(
            cells[6].text.strip().replace("$", "").replace(",", "")
        )
        if row_dict["cost"] == 0:
            continue

        row_dict[common_objects.CARD_NAME_COLUMN] = (
            cells[3].text.strip().replace("\n", "").replace("       ", "")
        )
        if "Code Card - " in row_dict[common_objects.CARD_NAME_COLUMN]:
            continue

        row_dict.update(common_objects.TCGSet(cells[4].text.strip()).to_dict())
        set_name = row_dict[common_objects.SET_NAME_COLUMN]

        card_name_cleanup(row_dict)

        url_card_link = row.find("a").get("href")
        if url_card_link:
            url_card_link_list = url_card_link.split("/")
            row_dict[common_objects.TCGP_ID_COLUMN] = int(url_card_link_list[-2])
            row_dict[common_objects.TCGP_PATH_COLUMN] = url_card_link_list[-1].split(
                "-", 1
            )[1]

        tcgp_id = row_dict[common_objects.TCGP_ID_COLUMN]
        if tcgp_id in table_data:
            # print("DUPE!")
            result = min(row_dict["cost"], table_data[tcgp_id]["cost"])
            if result == row_dict["cost"]:
                table_data[tcgp_id] = row_dict
        else:
            table_data[tcgp_id] = row_dict

    # for i in table_data:
    #     print(i, table_data[i])
    # print(
    #     f"Actual: {len(table_data)}, Expected: {common_objects.get_set_card_count(set_name)}"
    # )
    # print(json.dumps(table_data, indent=4))
    print(f"{len(table_data)}/{common_objects.get_set_card_count(set_name)}", set_name)
    # assert len(table_data) == common_objects.get_set_card_count(set_name)
    return table_data


def load_tcg_card_webpage(card_tcgp_id, card_tcgp_name):
    url = f"https://www.tcgplayer.com/product/{card_tcgp_id}/pokmeon-{card_tcgp_name}"
    print(url)


def get_html_soup_from_path(file_path):
    return BeautifulSoup(read_file(file_path), "html.parser")


def get_html_soup_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if request fails

    # Parse the HTML content
    return BeautifulSoup(response.content, "html.parser")


def load_set_data_dir(folder_path):
    set_htmls_path = pathlib.Path(folder_path)
    for html_path in list(sorted(set_htmls_path.rglob("*.html"))):
        yield extract_set_htmls(get_html_soup_from_path(html_path))


def load_set_list_data_dir(folder_path):
    set_htmls_path = pathlib.Path(folder_path)
    for html_path in list(sorted(set_htmls_path.rglob("*.html"))):
        yield extract_set_list_htmls(get_html_soup_from_path(html_path))


def get_pedia_set_data(set_list_htmls_path):
    html_path = set_list_htmls_path.replace(":", "")
    if pathlib.Path(html_path).resolve().exists():
        return extract_set_list_htmls(get_html_soup_from_path(html_path))


def get_all_cards_matching_name(card_name, card_list):
    ret_list = []
    for card in card_list:
        if card.get(common_objects.CARD_NAME_COLUMN) == card_name:
            ret_list.append(card)
        # elif card_name in card.get(common_objects.CARD_NAME_COLUMN):
        #     ret_list.append(card)
    if len(ret_list) == 0:
        print("Break")
    return ret_list
