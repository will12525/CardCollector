import pathlib

import requests
from bs4 import BeautifulSoup
import re
from app.utils import common_objects
from app.utils.common import Pack

SET_HTMLS = "set_htmls/"
SET_LIST_HTMLS = "set_list_htmls/"


def read_file(file_path):
    with open(file_path, "r") as f:
        output = f.read()
    return output


def get_html_soup_from_path(file_path):
    return BeautifulSoup(read_file(file_path), "html.parser")


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
    input_str = input_str.replace("â€”", "")
    input_str = re.sub(r"[\[\]()]", "", input_str)
    # if str("\\") in input_str:
    #     print(input_str)
    return input_str


def extract_card_index(card_index_str) -> int:
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


def get_trainer_subtype(card_type_str):
    if re.search(r"T \[St]", card_type_str):
        return "stadium"
    elif re.search(r"T \[TM]", card_type_str):
        return "technical Machine"
    elif re.search(r"T \[Su]", card_type_str):
        return "support"
    elif re.search(r"T \[PT]", card_type_str):
        return "pokemon tool"
    elif re.search(r"T\n", card_type_str):
        return None
    elif re.search(r"Su\n", card_type_str):
        return "support"
    elif re.search(r"St\n", card_type_str):
        return "stadium"
    elif re.search(r"E\n", card_type_str):
        return "energy"

    return None


class SetListCardData:
    card_name = ""
    card_type = ""
    card_rarity = ""
    card_index = 0
    card_index_unmodified = ""
    card_class = "creature"
    card_sub_class = ""
    cells = None

    def __init__(self, table_row_cells):
        # This whole file feels like gross spaghetti...
        self.cells = table_row_cells
        # print(table_row_cells)
        # row_dict[common_objects.CARD_INDEX_COLUMN] = cells[0].text.strip()
        self.card_name = extract_string(table_row_cells[2].text)

        card_type_a = table_row_cells[5].find("a")
        card_type_img = table_row_cells[5].find("img")
        card_type_text = extract_string(table_row_cells[5].text)
        if card_type_text:
            self.card_class = "trainer"
            self.card_sub_class = get_trainer_subtype(table_row_cells[5].text)
        elif card_type_a and card_type_a.has_attr("title"):
            self.card_type = str(card_type_a.get("title"))
        elif card_type_img and card_type_img.has_attr("title"):
            self.card_type = str(card_type_img.get("title"))
        else:
            print("Missing type")

        card_rarity_a = table_row_cells[3].find("a")
        card_rarity_text = extract_string(table_row_cells[3].text)
        if card_rarity_a and card_rarity_a.has_attr("title"):
            self.card_rarity = extract_string(card_rarity_a.get("title"))
        elif card_rarity_text:
            print(card_rarity_text)
        else:
            print("Missing rarity")

        self.card_index_unmodified = table_row_cells[0].text.strip()
        self.card_index = extract_card_index(self.card_index_unmodified)
        card_name_words = self.card_name.lower().split()
        if card_name_words[-1] == "energy":
            self.card_class = "energy"
            if self.card_rarity != "Common":
                self.card_sub_class = "special"

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
                "card_class": self.card_class,
            }
        return {
            "card_name": self.card_name,
            "card_rarity": self.card_rarity,
            "card_index": self.card_index,
            "card_class": self.card_class,
        }


class SetListSetData:
    card_list = None
    set_name = ""

    def __init__(self, set_name, html_path):
        self.set_name = set_name
        self.card_list = []
        html_soup = get_html_soup_from_path(html_path)

        # Check if table exists
        if table := html_soup.find("tbody"):
            # Extract headers and table data
            for row in table.find_all("tr"):
                th_cells = row.find_all("th")
                cells = row.find_all("td")
                if cells and len(cells) > 0:
                    cells.extend(th_cells)
                    if len(cells) == 6:
                        new_card = SetListCardData(cells)
                        self.card_list.append(new_card)

    def get_all_cards_matching_name(self, card_name):
        ret_list = []
        for card in self.card_list:
            if card.card_name == card_name:
                ret_list.append(card)
            # elif card_name in card.get("card_name"):
            #     ret_list.append(card)
        # if len(ret_list) == 0:
        #     print("Break")
        return ret_list

    def get_cards_with_index(self, card_index):
        ret_list = []
        for card in self.card_list:
            if card.card_index == card_index:
                ret_list.append(card)
        return ret_list

    def merge_cards(self, new_card, card_match):
        new_card.card_index = card_match.card_index
        new_card.rarity = card_match.card_rarity
        new_card.card_type = card_match.card_type
        new_card.card_class = card_match.card_class

    def compare_rarity(self, new_card, compare_card_list):
        selected_match = None
        for card_match in compare_card_list:
            if new_card.rarity.lower() in card_match.card_rarity.lower():
                if not selected_match:
                    selected_match = card_match
                else:
                    selected_match = None
                    break
        if selected_match:
            self.merge_cards(new_card, selected_match)

    def find_index(self, new_card):
        # print(json.dumps(new_card.to_dict(), indent=4))
        # Check for index
        if new_card.card_index:
            set_list_cards = self.get_cards_with_index(new_card.card_index)
            if len(set_list_cards) == 1:
                self.merge_cards(new_card, set_list_cards[0])
                # new_card.rarity = set_list_cards[0].card_rarity
                # new_card.card_type = set_list_cards[0].card_type
            else:
                self.compare_rarity(new_card, set_list_cards)
                print("Break")

        else:
            # if not new_card.card_index:
            found_card_matches = self.get_all_cards_matching_name(new_card.card_name)
            # print(json.dumps(new_card, indent=4))
            # print(
            #     "https://www.tcgplayer.com/product/"
            #     + str(new_card.tcgp_id)
            #     + "/pokmeon-"
            #     + new_card.tcgp_path
            # )
            # filtered_card_matches = []
            # for card_match in found_card_matches:
            #     if not db_getter_connection.get_card_with_set_index(
            #             {
            #                 common_objects.CARD_INDEX_COLUMN: card_match.get(
            #                     common_objects.CARD_INDEX_COLUMN
            #                 ),
            #                 common_objects.SET_ID_COLUMN: set_item.get(
            #                     "id"
            #                 ),
            #             }
            #     ):
            #         filtered_card_matches.append(card_match)

            if len(found_card_matches) == 1:
                # new_card.card_index = found_card_matches[0].card_index
                # new_card.rarity = found_card_matches[0].card_rarity
                # new_card.card_type = found_card_matches[0].card_type
                self.merge_cards(new_card, found_card_matches[0])

                # print(new_card)
            else:
                if new_card.rarity:
                    self.compare_rarity(new_card, found_card_matches)
                    # selected_match = None
                    # for card_match in found_card_matches:
                    #     if new_card.rarity.lower() in card_match.card_rarity.lower():
                    #         if not selected_match:
                    #             selected_match = card_match
                    #         else:
                    #             selected_match = None
                    #             break
                    # if selected_match:
                    #     self.merge_cards(new_card, selected_match)

                if not new_card.card_index:
                    # print(
                    #     "Possible matches: ",
                    #     "\n".join([str(card.to_dict()) for card in found_card_matches]),
                    # )
                    # provided_index = int(input("Provide index: ").replace("\n", "").strip())
                    # if provided_index:
                    #     print(f"Applying provided index: {provided_index}")
                    #     # print(type(provided_index))
                    #     new_card[common_objects.CARD_INDEX_COLUMN] = provided_index
                    return 1
        return 0

    def get_types(self):
        ret_dict = {}
        for card in self.card_list:
            if card.card_type in ret_dict:
                ret_dict[card.card_type] += 1
            else:
                ret_dict[card.card_type] = 1
        return ret_dict

    def get_rarities(self):
        ret_dict = {}
        for card in self.card_list:
            if card.card_rarity in ret_dict:
                ret_dict[card.card_rarity] += 1
            else:
                ret_dict[card.card_rarity] = 1
        return ret_dict

    def get_broken_indices(self):
        ret_dict = {}
        full_indices_dict = {}
        for card in self.card_list:
            if card.card_index in full_indices_dict:
                full_indices_dict[card.card_index] += 1
            else:
                full_indices_dict[card.card_index] = 1

        for key, value in full_indices_dict.items():
            if key == "" or value > 1:
                ret_dict[key] = value

        return ret_dict

    def to_dict(self):
        return [card.to_dict() for card in self.card_list]


def load_set_list_data_dir(data_path):
    set_htmls_path = pathlib.Path(f"{data_path}{SET_LIST_HTMLS}")
    for html_path in list(set_htmls_path.rglob("*.html")):
        yield SetListSetData(html_path.stem, html_path)


def load_set_list_from_name(data_path, set_name):
    modified_set_name = set_name.replace(":", "")
    html_path = pathlib.Path(f"{data_path}{SET_LIST_HTMLS}{modified_set_name}.html")
    if html_path.resolve().exists():
        return SetListSetData(set_name, html_path)


class CardData:
    card_name = ""
    price = 0
    rarity = ""
    card_index = None
    tcgp_id = None
    tcgp_path = ""
    set_id = None
    set_name = ""
    card_type = ""
    card_class = ""
    cost = None
    cells = None

    def __init__(self, row):
        table_row = row.find_all(["td", "th"])
        self.cells = table_row
        self.cost = float(table_row[6].text.strip().replace("$", "").replace(",", ""))

        self.card_name = (
            table_row[3].text.strip().replace("\n", "").replace("       ", "")
        )

        self.set_name = table_row[4].text.strip()
        if "Code Card - " not in self.card_name:
            self.card_name_cleanup()

        url_card_link = row.find("a").get("href")
        if url_card_link:
            url_card_link_list = url_card_link.split("/")
            self.tcgp_id = int(url_card_link_list[-2])
            self.tcgp_path = url_card_link_list[-1].split("-", 1)[1]

    def card_name_cleanup(self):
        card_foil_pattern = r"- \[(.+)\]$"
        card_index_dash_division_pattern = r"- (\d+)/\d+"
        card_index_division_pattern = r" (\d+)/\d+"
        card_index_sub_division_pattern = r" -(\d+)/\d+"
        card_index_sub_pattern = r"- (\d+)-\d+"
        card_index_pattern = r" \((\d+)\)"
        card_index_H_pattern = r" \(H(\d+)\)"
        card_index_a_category_pattern = r" \((\d+)a\)"
        card_index_b_category_pattern = r" \((\d+)b\)"
        card_index_AR_category_pattern = r" \(AR(\d+)\)"
        # card_rarity_pattern = r"\(([^0-9()]+)\)"
        card_rarity_pattern = r"\((\d+)?([^0-9()]+)\)"
        card_index_rarity_pattern = r"(.*) \(.*- (\d+)\s*(.*)\)"
        special_characters_pattern = r"[^a-zA-Z0-9'\.\-\&\s]"
        if card_rarity_search := re.search(card_foil_pattern, self.card_name):
            self.rarity = card_rarity_search.groups()[-1]
            self.card_name = self.card_name[: card_rarity_search.span()[0]].strip()
        if card_index_search := re.search(
            card_index_dash_division_pattern, self.card_name
        ):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(card_index_division_pattern, self.card_name):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(
            card_index_sub_division_pattern, self.card_name
        ):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(card_index_sub_pattern, self.card_name):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(card_index_pattern, self.card_name):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(card_index_H_pattern, self.card_name):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(
            card_index_a_category_pattern, self.card_name
        ):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(
            card_index_AR_category_pattern, self.card_name
        ):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(
            card_index_b_category_pattern, self.card_name
        ):
            self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()

        if card_index_search := re.search(card_rarity_pattern, self.card_name):
            self.rarity = card_index_search.groups()[1].strip()
            if card_index_search.groups()[0]:
                self.card_index = int(card_index_search.groups()[0])
            self.card_name = self.card_name[: card_index_search.span()[0]].strip()
        if card_index_search := re.search(card_index_rarity_pattern, self.card_name):
            self.card_name = card_index_search.group(1)
            self.card_index = int(card_index_search.group(2))
            self.rarity = card_index_search.group(3).strip()

        # if "(" in self.card_name:
        #     print("Break")
        self.card_name = re.sub(r"[\[\]()]", "", self.card_name)
        self.rarity = self.rarity.replace("Holofoil", "").replace("Reverse", "").strip()
        # if "holo" in self.rarity.lower():
        #     # input(self.rarity)
        #     self.rarity = "holo"

    def to_dict(self):
        card_dict = {
            "card_name": self.card_name,
            "card_type": self.card_type,
            "card_rarity": self.rarity,
            "card_index": self.card_index,
            "id": self.set_id,
            "tcgp_id": self.tcgp_id,
            "tcgp_path": self.tcgp_path,
            "card_class": self.card_class,
        }
        # card_dict.update(self.card_set.to_dict())
        return card_dict


class SetDataList:
    card_list = None
    card_dict = None
    set_name = ""
    set_index = None
    set_card_count = None
    set_id = None
    set_list_data = None

    def __init__(self, data_path, html_path):
        self.card_list = []
        self.card_dict = {}
        html_soup = get_html_soup_from_path(html_path)
        table = html_soup.find("tbody")

        # Check if table exists
        if table:
            for row in table.find_all("tr"):
                card_data = CardData(row)
                if not self.set_name:
                    self.populate_set_data(data_path, card_data.set_name)

                if "Code Card - " in card_data.card_name:
                    continue
                if "1st Edition" in card_data.rarity or "Unlimited" in card_data.rarity:
                    continue

                if card_data.tcgp_id in self.card_dict:
                    # print("DUPE!")
                    result = min(
                        card_data.cost, self.card_dict.get(card_data.tcgp_id).cost
                    )
                    if result == card_data.cost:
                        self.card_dict[card_data.tcgp_id] = card_data
                else:
                    self.card_dict[card_data.tcgp_id] = card_data

                # self.set_list_data.find_index(card_data)

            print(
                f"{len(self.card_dict)}/{self.set_card_count}",
                self.set_name,
            )

        for key in self.card_dict:
            self.set_list_data.find_index(self.card_dict[key])

    def populate_set_data(self, data_path, set_name):
        self.set_name = set_name
        self.set_index = common_objects.get_set_index(set_name)
        self.set_card_count = common_objects.get_set_card_count(set_name)
        if not self.set_list_data:
            self.set_list_data = load_set_list_from_name(data_path, self.set_name)

    def clear_dupes(self):
        pass

    def to_dict(self):
        return {
            "set_id": self.set_id,
            "set_name": self.set_name,
            "set_index": self.set_index,
            "set_card_count": self.set_card_count,
            "set_found_card_count": self.set_card_count,
        }


def load_tcg_card_webpage(card_tcgp_id, card_tcgp_name):
    url = f"https://www.tcgplayer.com/product/{card_tcgp_id}/pokmeon-{card_tcgp_name}"
    print(url)


def get_html_soup_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if request fails

    # Parse the HTML content
    return BeautifulSoup(response.content, "html.parser")


def load_set_data_dir(data_path):
    set_htmls_path = pathlib.Path(f"{data_path}{SET_HTMLS}")
    for html_path in list(sorted(set_htmls_path.rglob("*.html"))):
        yield SetDataList(data_path, html_path)


def load_set_data(data_path, set_name):
    modified_set_name = set_name.replace(":", "")
    html_path = pathlib.Path(f"{data_path}{SET_HTMLS}{modified_set_name}.html")
    if html_path.resolve().exists():
        return SetDataList(data_path, html_path)
