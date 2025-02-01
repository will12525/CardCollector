# Table names
from enum import Enum, auto

ID_COLUMN = "id"


CARD_INFO_TABLE = "card_info"
CARD_NAME_COLUMN = "card_name"
CARD_TYPE_COLUMN = "card_type"
CARD_TYPE2_COLUMN = "card_type2"
CARD_RARITY_COLUMN = "card_rarity"
CARD_INDEX_COLUMN = "card_index"
TCGP_ID_COLUMN = "tcgp_id"
TCGP_PATH_COLUMN = "tcgp_path"
SET_ID_COLUMN = "set_id"
CARD_CLASS_COLUMN = "card_class"

SET_INFO_TABLE = "set_info"
SET_NAME_COLUMN = "set_name"
SET_INDEX_COLUMN = "set_index"
SET_CARD_COUNT_COLUMN = "set_card_count"

USER_INFO_TABLE = "user_info"
USER_NAME_COLUMN = "user_name"


USER_COLLECTION_TABLE = "user_collection"
USER_ID_COLUMN = "user_id"
CARD_ID_COLUMN = "card_id"
OWN_COUNT_COLUMN = "own_count"
STATE_WANT_COLUMN = "state_want"
STATE_GIFT_COLUMN = "state_gift"

PRICE_COLUMN = "price"


default_card_dict = {
    CARD_NAME_COLUMN: "",
    SET_NAME_COLUMN: "",
    SET_ID_COLUMN: "",
    SET_INDEX_COLUMN: 0,
    CARD_TYPE_COLUMN: "",
    CARD_RARITY_COLUMN: "",
    CARD_INDEX_COLUMN: None,
    TCGP_ID_COLUMN: 0,
    TCGP_PATH_COLUMN: "",
    CARD_CLASS_COLUMN: "",
}


class CardInfo:
    state_have = False
    state_want = False
    card_name = ""
    set_name = ""
    price_mid = 0
    card_rarity = ""
    card_index = ""
    state_gift = 0
    tcgp_id = 0
    tcg_path = ""

    def __init__(self):
        self.card_index = 1

    # def get_db_insert(self):


class DBType(Enum):
    PHYSICAL = auto()
    MEMORY = auto()


card_rarities = {
    "Common": 0.4,
    "Uncommon": 0.3,
    "Rare": 0.01,
}
rare_sub_types = {
    "Rare": 0.01,
    "Rare Holo": 0.01,
    "Rare Holo LV.X": 0.01,
    "Rare Holo ex": 0.01,
    "Rare Holo star": 0.01,
    "Rare Secret": 0.008,
    "Rare Ultra": 0.008,
    "Rare Ace": 0.01,
    "Delta Species": 0.01,
    "Prime": 0.01,
    "Full Art": 0.005,
    "Team Plasma": 0.01,
    "Shining Holo": 0.01,
    "SuperRare Holo": 0.005,
    "Secret": 0.003,
    "Alternate Full Art": 0.005,
    "Secret Rare": 0.001,
    "Double Rare": 0.01,
    "Ultra Rare": 0.0001,
    "Illustration Rare": 0.005,
    "Special Illustration Rare": 0.001,
    "Cosmos Holo": 0.01,
    "Hyper Rare": 0.0001,
    "ACE SPEC Rare": 0.01,
    "Cracked Ice Holo": 0.01,
    "Alternate Art Secret": 0.0001,
    "Ultra-Rare Rare": 0.01,
    "TGU": 0.01,
    "TGH": 0.01,
    "Shiny": 0.01,
    "Rare Rainbow": 0.0001,
    "Rare Radiant": 0.01,
    "Shiny Full Art": 0.0001,
    "Alpha": 0.01,
    "Omega": 0.01,
}

tcgp_set_info = {
    "Base Set (Shadowless)": {"card_count": 102, "set_index": 1},
    "Jungle": {"card_count": 64, "set_index": 2},
    "Fossil": {"card_count": 62, "set_index": 3},
    "Base set 2": {"card_count": 130, "set_index": 4},
    "Team Rocket": {"card_count": 83, "set_index": 5},
    "Gym Heroes": {"card_count": 132, "set_index": 6},
    "Gym Challenge": {"card_count": 132, "set_index": 7},
    "Neo Genesis": {"card_count": 111, "set_index": 8},
    "Neo Discovery": {"card_count": 75, "set_index": 9},
    "Neo Revelation": {"card_count": 66, "set_index": 10},
    "Neo Destiny": {"card_count": 113, "set_index": 11},
    "Legendary Collection": {"card_count": 110, "set_index": 12},
    "Expedition": {"card_count": 165, "set_index": 13},
    "Aquapolis": {"card_count": 186, "set_index": 14},
    "Skyridge": {"card_count": 182, "set_index": 15},
    "Ruby and Sapphire": {"card_count": 109, "set_index": 16},
    "Sandstorm": {"card_count": 100, "set_index": 17},
    "Dragon": {"card_count": 100, "set_index": 18},
    "Team Magma vs Team Aqua": {"card_count": 97, "set_index": 19},
    "Hidden Legends": {"card_count": 102, "set_index": 20},
    "FireRed & LeafGreen": {"card_count": 116, "set_index": 21},
    "Team Rocket Returns": {"card_count": 111, "set_index": 22},
    "Deoxys": {"card_count": 108, "set_index": 23},
    "Emerald": {"card_count": 107, "set_index": 24},
    "Unseen Forces": {"card_count": 145, "set_index": 25},
    "Delta Species": {"card_count": 114, "set_index": 26},
    "Legend Maker": {"card_count": 93, "set_index": 27},
    "Holon Phantoms": {"card_count": 111, "set_index": 28},
    "Crystal Guardians": {"card_count": 100, "set_index": 29},
    "Dragon Frontiers": {"card_count": 101, "set_index": 30},
    "Power Keepers": {"card_count": 108, "set_index": 31},
    "Diamond and Pearl": {"card_count": 130, "set_index": 32},
    "Mysterious Treasures": {"card_count": 124, "set_index": 33},
    "Secret Wonders": {"card_count": 132, "set_index": 34},
    "Great Encounters": {"card_count": 106, "set_index": 35},
    "Majestic Dawn": {"card_count": 100, "set_index": 36},
    "Legends Awakened": {"card_count": 146, "set_index": 37},
    "Stormfront": {"card_count": 106, "set_index": 38},
    "Platinum": {"card_count": 133, "set_index": 39},
    "Rising Rivals": {"card_count": 120, "set_index": 40},
    "Supreme Victors": {"card_count": 153, "set_index": 41},
    "Arceus": {"card_count": 111, "set_index": 42},
    "HeartGold SoulSilver": {"card_count": 124, "set_index": 43},
    "Unleashed": {"card_count": 96, "set_index": 44},
    "Undaunted": {"card_count": 91, "set_index": 45},
    "Triumphant": {"card_count": 103, "set_index": 46},
    "Call of Legends": {"card_count": 106, "set_index": 47},
    "Black and White": {"card_count": 115, "set_index": 48},
    "Emerging Powers": {"card_count": 98, "set_index": 49},
    "Noble Victories": {"card_count": 102, "set_index": 50},
    "Next Destinies": {"card_count": 103, "set_index": 51},
    "Dark Explorers": {"card_count": 111, "set_index": 52},
    "Dragons Exalted": {"card_count": 128, "set_index": 53},
    "Boundaries Crossed": {"card_count": 153, "set_index": 54},
    "Plasma Storm": {"card_count": 138, "set_index": 55},
    "Plasma Freeze": {"card_count": 122, "set_index": 56},
    "Plasma Blast": {"card_count": 105, "set_index": 57},
    "Legendary Treasures": {"card_count": 115, "set_index": 58},
    "Legendary Treasures: Radiant Collection": {"card_count": 25, "set_index": 59},
    "XY Base Set": {"card_count": 146, "set_index": 60},
    "XY - Flashfire": {"card_count": 109, "set_index": 61},
    "XY - Furious Fists": {"card_count": 113, "set_index": 62},
    "XY - Phantom Forces": {"card_count": 122, "set_index": 63},
    "XY - Primal Clash": {"card_count": 164, "set_index": 64},
    "XY - Roaring Skies": {"card_count": 110, "set_index": 65},
    "XY - Ancient Origins": {"card_count": 100, "set_index": 66},
    "XY - BREAKthrough": {"card_count": 164, "set_index": 67},
    "XY - BREAKpoint": {"card_count": 123, "set_index": 68},
    "XY - Fates Collide": {"card_count": 125, "set_index": 69},
    "XY - Steam Siege": {"card_count": 116, "set_index": 70},
    "XY - Evolutions": {"card_count": 113, "set_index": 71},
    "SM Base Set": {"card_count": 163, "set_index": 72},
    "SM - Guardians Rising": {"card_count": 169, "set_index": 73},
    "SM - Burning Shadows": {"card_count": 169, "set_index": 74},
    "SM - Crimson Invasion": {"card_count": 124, "set_index": 75},
    "SM - Ultra Prism": {"card_count": 173, "set_index": 76},
    "SM - Forbidden Light": {"card_count": 146, "set_index": 77},
    "SM - Celestial Storm": {"card_count": 183, "set_index": 78},
    "SM - Lost Thunder": {"card_count": 236, "set_index": 79},
    "SM - Team Up": {"card_count": 196, "set_index": 80},
    "SM - Unbroken Bonds": {"card_count": 234, "set_index": 81},
    "SM - Unified Minds": {"card_count": 258, "set_index": 82},
    "SM - Cosmic Eclipse": {"card_count": 271, "set_index": 83},
    "SWSH01: Sword & Shield Base Set": {"card_count": 216, "set_index": 84},
    "SWSH02: Rebel Clash": {"card_count": 209, "set_index": 85},
    "SWSH03: Darkness Ablaze": {"card_count": 201, "set_index": 86},
    "SWSH04: Vivid Voltage": {"card_count": 203, "set_index": 87},
    "SWSH05: Battle Styles": {"card_count": 183, "set_index": 88},
    "SWSH06: Chilling Reign": {"card_count": 233, "set_index": 89},
    "SWSH07: Evolving Skies": {"card_count": 237, "set_index": 90},
    "SWSH08: Fusion Strike": {"card_count": 284, "set_index": 91},
    "SWSH09: Brilliant Stars": {"card_count": 186, "set_index": 92},
    "SWSH09: Brilliant Stars Trainer Gallery": {"card_count": 30, "set_index": 93},
    "SWSH10: Astral Radiance": {"card_count": 216, "set_index": 94},
    "SWSH10: Astral Radiance Trainer Gallery": {"card_count": 30, "set_index": 95},
    "SWSH11: Lost Origin": {"card_count": 217, "set_index": 96},
    "SWSH11: Lost Origin Trainer Gallery": {"card_count": 30, "set_index": 97},
    "SWSH12: Silver Tempest": {"card_count": 215, "set_index": 98},
    "SWSH12: Silver Tempest Trainer Gallery": {"card_count": 30, "set_index": 99},
    "SV01: Scarlet & Violet Base Set": {
        "card_count": 258,
        "set_index": 100,
        "pack_data": {
            "card_count": 10,
            "probabilities": [{"common": 3, "chance": 20}],
        },
    },
    "SV02: Paldea Evolved": {"card_count": 279, "set_index": 101},
    "SV03: Obsidian Flames": {"card_count": 230, "set_index": 102},
    "SV04: Paradox Rift": {"card_count": 266, "set_index": 103},
    "SV05: Temporal Forces": {"card_count": 218, "set_index": 104},
    "SV06: Twilight Masquerade": {"card_count": 226, "set_index": 105},
    "SV07: Stellar Crown": {"card_count": 170, "set_index": 106},
    "SV08: Surging Sparks": {"card_count": 252, "set_index": 107},
}

creature_types = [
    "darkness",
    # "metal",
    "fighting",
    "fire",
    "grass",
    "lightning",
    "psychic",
    "water",
    "rainbow",
]


def check_energy_card(card_name: str) -> bool:
    lower_card_name = card_name.lower()
    for creature_type in creature_types:
        if lower_card_name == f"{creature_type} energy":
            return True
    return False


def get_set_name_list():
    return tcgp_set_info.keys()


def get_set_index(set_name):
    return tcgp_set_info.get(set_name, {}).get("set_index")


def get_set_name_from_index(set_index):
    for set_name, set_info in tcgp_set_info.items():
        if set_info.get("set_index") == set_index:
            return set_name


def get_set_card_count(set_name):
    return tcgp_set_info.get(set_name, {}).get("card_count")


def get_set_count():
    return len(tcgp_set_info)


def get_total_card_count():
    card_sum = 0
    for set_info in tcgp_set_info.values():
        card_sum += set_info.get("card_count")
    return card_sum
