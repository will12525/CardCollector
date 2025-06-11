INSERT_IGNORE = "INSERT OR IGNORE INTO"
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS"

# f"UPDATE card_info SET card_type = 1 WHERE tcgp_id=:tcgp_id;"
SORT_ALPHABETICAL = "GLOB '[A-Za-z]*'"

"""
SCHEMA QUERIES
"""
sql_create_version_info_table = f"""CREATE TABLE IF NOT EXISTS version_info (
                                     id integer PRIMARY KEY,
                                     version integer NOT NULL
                                  );"""
sql_insert_version_info_table = (
    "INSERT INTO version_info(version) VALUES(:version_info);"
)
version_info_query = "SELECT version FROM version_info;"

sql_create_card_info_table = f"""{CREATE_TABLE} card_info (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    card_name TEXT NOT NULL COLLATE NOCASE,
                                    set_id integer NOT NULL,
                                    card_type text DEFAULT "",
                                    card_rarity text DEFAULT "",
                                    card_index integer,
                                    tcgp_id integer NOT NULL UNIQUE,
                                    tcgp_path text NOT NULL,
                                    card_class text NOT NULL,
                                    attack_info TEXT DEFAULT '',
                                    energy_cost TEXT DEFAULT '',
                                    card_text TEXT DEFAULT '',
                                    FOREIGN KEY (set_id) REFERENCES set_info (id)
                                );"""

sql_insert_card_info_table = f"INSERT INTO card_info (card_name, set_id, card_type, card_rarity, card_index, tcgp_id, tcgp_path, card_class) VALUES (:card_name, :set_id, :card_type, :card_rarity, :card_index, :tcgp_id, :tcgp_path, :card_class);"

sql_create_set_info_table = f"""{CREATE_TABLE} set_info (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    set_name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                                    set_index integer UNIQUE,
                                    set_card_count integer NOT NULL
                                );"""

sql_insert_set_info_table = f"{INSERT_IGNORE} set_info (set_name, set_index, set_card_count) VALUES (:set_name, :set_index, :set_card_count);"

sql_create_user_info_table = f"""{CREATE_TABLE} user_info (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user_name TEXT NOT NULL UNIQUE,
                                    user_pass_hash TEXT NOT NULL,
                                    last_pack_open_time TEXT DEFAULT "",
                                    last_set_name TEXT DEFAULT "",
                                    last_deck_id integer
                                );"""
sql_insert_user_info_table = f"INSERT INTO user_info (user_name, user_pass_hash) VALUES (:user_name, :user_pass_hash);"


sql_create_user_collection_table = f"""{CREATE_TABLE} user_collection (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    user_id integer NOT NULL,
                                    card_id integer NOT NULL,
                                    own_count integer NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES user_info (id),
                                    FOREIGN KEY (card_id) REFERENCES card_info (id)
                                    UNIQUE (user_id, card_id)
                                );"""

sql_insert_user_collection_table = f"{INSERT_IGNORE} user_collection (user_id, card_id, own_count) VALUES (:user_id, :card_id, :own_count);"
delete_users = f"DELETE FROM user_info;"
sql_create_deck_info_table = f"""
                {CREATE_TABLE} deck_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    deck_name TEXT DEFAULT "",
                    FOREIGN KEY (user_id) REFERENCES user_info (id)
                );
            """
delete_deck_info = f"DELETE FROM deck_info;"
sql_create_deck_cards_info_table = f"""
                {CREATE_TABLE} deck_cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    deck_id INTEGER NOT NULL,
                    card_id INTEGER NOT NULL,
                    card_count INTEGER NOT NULL,
                    FOREIGN KEY (deck_id) REFERENCES deck_info (id),
                    FOREIGN KEY (card_id) REFERENCES card_info (id),
                    UNIQUE (deck_id, card_id)
                );
            """
delete_deck_cards = f"DELETE FROM deck_cards;"
sql_create_ban_info_table = f"""
                {CREATE_TABLE} ban_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_id INTEGER NOT NULL UNIQUE,
                    ban_reason TEXT DEFAULT '',
                    FOREIGN KEY (card_id) REFERENCES card_info (id)
                );
            """


get_set_id_from_name = f"SELECT id FROM set_info WHERE set_name=:set_name;"

"""
CARD QUERIES
"""
get_card_from_id = f"SELECT * FROM card_info WHERE tcgp_id=:tcgp_id;"
get_card_info = f"SELECT * FROM card_info WHERE id=:card_id;"
get_all_ids = f"SELECT tcgp_id FROM card_info;"
get_card_with_set_index = (
    f"SELECT tcgp_id FROM card_info WHERE set_id=:set_id AND card_index=:card_index;"
)
search_card_names = f"SELECT * FROM card_info WHERE UPPER(card_name) LIKE UPPER(?);"

"""
CARD SORT ORDERS
"""
sort_index_asc = (
    f"ORDER BY card_info.card_index ASC NULLS LAST, set_info.set_index, card_name"
)
sort_index_desc = f"ORDER BY card_info.card_index DESC NULLS LAST, set_info.set_index DESC, card_name DESC"
sort_name_alpha_asc = f"ORDER BY card_name"
sort_name_alpha_desc = f"ORDER BY card_name DESC"
sort_own_desc = f"ORDER BY own_count DESC"

"""
USER COLLECTION QUERIES
"""
collection_base_query = f"FROM card_info INNER JOIN set_info ON card_info.set_id = set_info.id LEFT JOIN user_collection ON card_info.id = user_collection.card_id AND user_collection.user_id = :user_id"
get_card_in_user_collection_count = f"SELECT own_count FROM user_collection WHERE user_id=:user_id AND card_id=:card_id;"
increment_card_in_user_collection = f"UPDATE user_collection SET own_count = own_count + 1 WHERE card_id=:card_id AND user_id=:user_id;"
add_card_to_user_collection = f"INSERT INTO user_collection (user_id, card_id, own_count) VALUES (:user_id, :card_id, 1);"
get_all_card_data = (
    f"SELECT * FROM card_info INNER JOIN set_info ON card_info.set_id = set_info.id;"
)
get_all_set_card_data = f"SELECT * FROM card_info INNER JOIN set_info ON card_info.set_id = set_info.id LEFT JOIN user_collection ON card_info.id = user_collection.card_id AND user_collection.user_id = :user_id WHERE set_name=:set_name;"

"""
PACK GENERATION QUERIES
"""
generate_random_pack = f"SELECT * FROM card_info ORDER BY RANDOM() LIMIT :card_count;"
generate_pack_from_set = f"SELECT * FROM card_info INNER JOIN set_info ON card_info.set_id = set_info.id WHERE set_info.set_name = :set_name ORDER BY RANDOM() LIMIT :card_count;"

"""
USER DATA QUERIES
"""
get_user_id = f"SELECT id FROM user_info WHERE user_name = :user_name;"
user_login = f"SELECT id FROM user_info WHERE user_name = :user_name AND user_pass_hash = :user_pass_hash;"
get_user_hash = (
    f"SELECT id, user_pass_hash FROM user_info WHERE user_name = :user_name;"
)
set_user_pack_time = f"UPDATE user_info SET last_pack_open_time = :last_pack_open_time WHERE user_name=:user_name AND id=:id;"
get_user_pack_time = f"SELECT last_pack_open_time FROM user_info WHERE user_name = :user_name AND id=:id;"
set_user_last_set = f"UPDATE user_info SET last_set_name = :set_name WHERE user_name=:user_name AND id=:user_id;"

"""
TCG SET QUERIES
"""
get_sets = f"SELECT * FROM set_info ORDER BY set_index ASC;"
get_set_card_count = (
    f"SELECT COUNT(*) AS set_card_count FROM card_info WHERE set_id=:id;"
)

"""
USER DECK QUERIES
"""
add_card_to_deck = f"""
            INSERT INTO deck_cards (deck_id, card_id, card_count)
            SELECT :deck_id, :card_id, 1
            WHERE EXISTS (
                SELECT 1 FROM deck_info
                WHERE deck_info.id = :deck_id AND deck_info.user_id = :user_id
            )
            ON CONFLICT(deck_id, card_id)
            DO UPDATE SET card_count = card_count + 1
            WHERE EXISTS (
                SELECT 1 FROM deck_info
                WHERE deck_info.id = :deck_id AND deck_info.user_id = :user_id
            );
        """
remove_card_from_deck = """
            DELETE FROM deck_cards
            WHERE card_id = :card_id AND deck_id = :deck_id AND card_count = 1;
        """
decrement_card_from_deck = """
            UPDATE deck_cards
            SET card_count = card_count - 1
            WHERE card_id = :card_id AND deck_id = :deck_id AND card_count > 1;
        """
create_deck = (
    f"INSERT INTO deck_info (user_id, deck_name) VALUES (:user_id, :deck_name);"
)
update_deck = f"UPDATE deck_info SET deck_name = :deck_name WHERE user_id=:user_id AND id=:deck_id;"
get_user_decks = f"SELECT * FROM deck_info WHERE user_id = :user_id;"
get_deck_cards = """
                SELECT card_info.*, deck_cards.card_count
                FROM deck_cards
                JOIN deck_info ON deck_cards.deck_id = deck_info.id
                JOIN card_info ON deck_cards.card_id = card_info.id
                WHERE deck_info.user_id = :user_id AND deck_info.id = :deck_id;
            """
get_deck_cards_card_count = (
    "SELECT card_count FROM deck_cards WHERE deck_id = :deck_id AND card_id = :card_id;"
)
get_deck_card_count = f"""
                    SELECT
                    SUM(deck_cards.card_count) AS card_count
                    FROM deck_cards
                    JOIN card_info ON deck_cards.card_id = card_info.id
                    WHERE deck_cards.deck_id = :deck_id;
                """
get_deck_info = f"SELECT * FROM deck_info WHERE id = :deck_id AND user_id = :user_id;"
