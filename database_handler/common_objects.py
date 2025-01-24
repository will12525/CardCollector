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


tcgp_set_info = [
    {"name": "Base Set (Shadowless)", "card_count": 102},
    {"name": "Jungle", "card_count": 64},
    {"name": "Fossil", "card_count": 62},
    {"name": "Base set 2", "card_count": 130},
    {"name": "Team Rocket", "card_count": 83},
    {"name": "Gym Heroes", "card_count": 132},
    {"name": "Gym Challenge", "card_count": 132},
    {"name": "Neo Genesis", "card_count": 111},
    {"name": "Neo Discovery", "card_count": 75},
    {"name": "Neo Revelation", "card_count": 66},
    {"name": "Neo Destiny", "card_count": 113},
    {"name": "Legendary Collection", "card_count": 110},
    {"name": "Expedition", "card_count": 165},
    {"name": "Aquapolis", "card_count": 186},
    {"name": "Skyridge", "card_count": 182},
    {"name": "Ruby and Sapphire", "card_count": 109},
    {"name": "Sandstorm", "card_count": 100},
    {"name": "Dragon", "card_count": 100},
    {"name": "Team Magma vs Team Aqua", "card_count": 97},
    {"name": "Hidden Legends", "card_count": 102},
    {"name": "FireRed & LeafGreen", "card_count": 116},
    {"name": "Team Rocket Returns", "card_count": 111},
    {"name": "Deoxys", "card_count": 108},
    {"name": "Emerald", "card_count": 107},
    {"name": "Unseen Forces", "card_count": 145},
    {"name": "Delta Species", "card_count": 114},
    {"name": "Legend Maker", "card_count": 93},
    {"name": "Holon Phantoms", "card_count": 111},
    {"name": "Crystal Guardians", "card_count": 100},
    {"name": "Dragon Frontiers", "card_count": 101},
    {"name": "Power Keepers", "card_count": 108},
    {"name": "Diamond and Pearl", "card_count": 130},
    {"name": "Mysterious Treasures", "card_count": 124},
    {"name": "Secret Wonders", "card_count": 132},
    {"name": "Great Encounters", "card_count": 106},
    {"name": "Majestic Dawn", "card_count": 100},
    {"name": "Legends Awakened", "card_count": 146},
    {"name": "Stormfront", "card_count": 106},
    {"name": "Platinum", "card_count": 133},
    {"name": "Rising Rivals", "card_count": 120},
    {"name": "Supreme Victors", "card_count": 153},
    {"name": "Arceus", "card_count": 111},
    {"name": "HeartGold SoulSilver", "card_count": 124},
    {"name": "Unleashed", "card_count": 96},
    {"name": "Undaunted", "card_count": 91},
    {"name": "Triumphant", "card_count": 103},
    {"name": "Call of Legends", "card_count": 106},
    {"name": "Black and White", "card_count": 115},
    {"name": "Emerging Powers", "card_count": 98},
    {"name": "Noble Victories", "card_count": 102},
    {"name": "Next Destinies", "card_count": 103},
    {"name": "Dark Explorers", "card_count": 111},
    {"name": "Dragons Exalted", "card_count": 128},
    {"name": "Boundaries Crossed", "card_count": 153},
    {"name": "Plasma Storm", "card_count": 138},
    {"name": "Plasma Freeze", "card_count": 122},
    {"name": "Plasma Blast", "card_count": 105},
    {"name": "Legendary Treasures", "card_count": 115},
    {"name": "Legendary Treasures: Radiant Collection", "card_count": 25},
    {"name": "XY Base Set", "card_count": 146},
    {"name": "XY - Flashfire", "card_count": 109},
    {"name": "XY - Furious Fists", "card_count": 113},
    {"name": "XY - Phantom Forces", "card_count": 122},
    {"name": "XY - Primal Clash", "card_count": 164},
    {"name": "XY - Roaring Skies", "card_count": 110},
    {"name": "XY - Ancient Origins", "card_count": 100},
    {"name": "XY - BREAKthrough", "card_count": 164},
    {"name": "XY - BREAKpoint", "card_count": 123},
    {"name": "XY - Fates Collide", "card_count": 125},
    {"name": "XY - Steam Siege", "card_count": 116},
    {"name": "XY - Evolutions", "card_count": 113},
    {"name": "SM Base Set", "card_count": 163},
    {"name": "SM - Guardians Rising", "card_count": 169},
    {"name": "SM - Burning Shadows", "card_count": 169},
    {"name": "SM - Crimson Invasion", "card_count": 124},
    {"name": "SM - Ultra Prism", "card_count": 173},
    {"name": "SM - Forbidden Light", "card_count": 146},
    {"name": "SM - Celestial Storm", "card_count": 183},
    {"name": "SM - Lost Thunder", "card_count": 236},
    {"name": "SM - Team Up", "card_count": 196},
    {"name": "SM - Unbroken Bonds", "card_count": 234},
    {"name": "SM - Unified Minds", "card_count": 258},
    {"name": "SM - Cosmic Eclipse", "card_count": 271},
    {"name": "SWSH01: Sword & Shield Base Set", "card_count": 216},
    {"name": "SWSH02: Rebel Clash", "card_count": 209},
    {"name": "SWSH03: Darkness Ablaze", "card_count": 201},
    {"name": "SWSH04: Vivid Voltage", "card_count": 203},
    {"name": "SWSH05: Battle Styles", "card_count": 183},
    {"name": "SWSH06: Chilling Reign", "card_count": 233},
    {"name": "SWSH07: Evolving Skies", "card_count": 237},
    {"name": "SWSH08: Fusion Strike", "card_count": 284},
    {"name": "SWSH09: Brilliant Stars", "card_count": 186},
    {"name": "SWSH09: Brilliant Stars Trainer Gallery", "card_count": 30},
    {"name": "SWSH10: Astral Radiance", "card_count": 216},
    {"name": "SWSH10: Astral Radiance Trainer Gallery", "card_count": 30},
    {"name": "SWSH11: Lost Origin", "card_count": 217},
    {"name": "SWSH11: Lost Origin Trainer Gallery", "card_count": 30},
    {"name": "SWSH12: Silver Tempest", "card_count": 215},
    {"name": "SWSH12: Silver Tempest Trainer Gallery", "card_count": 30},
    {"name": "SV01: Scarlet & Violet Base Set", "card_count": 258},
    {"name": "SV02: Paldea Evolved", "card_count": 279},
    {"name": "SV03: Obsidian Flames", "card_count": 230},
    {"name": "SV04: Paradox Rift", "card_count": 266},
    {"name": "SV05: Temporal Forces", "card_count": 218},
    {"name": "SV06: Twilight Masquerade", "card_count": 226},
    {"name": "SV07: Stellar Crown", "card_count": 170},
    {"name": "SV08: Surging Sparks", "card_count": 252},
]


def get_set_name_list():
    return [item["name"] for item in tcgp_set_info]


def get_set_index(set_name):
    set_name_list = get_set_name_list()
    if set_name in set_name_list:
        return set_name_list.index(set_name) + 1
    return None


def get_set_name_from_index(set_index):
    print(set_index)
    if set_index < len(tcgp_set_info):
        return tcgp_set_info[set_index - 1].get("name")
    return None


def get_set_card_count(set_name):
    for set_info in tcgp_set_info:
        if set_info.get("name", "") == set_name:
            return set_info.get("card_count", "")
    return None


def get_set_count():
    return len(tcgp_set_info)


class TCGSet:
    set_name = ""
    set_index = None
    set_card_count = None

    def __init__(self, set_name):
        self.set_name = set_name
        self.set_index = get_set_index(set_name)
        self.set_card_count = get_set_card_count(set_name)

    def to_dict(self):
        return {
            "set_name": self.set_name,
            "set_index": self.set_index,
            "set_card_count": self.set_card_count,
        }
