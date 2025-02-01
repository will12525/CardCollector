import json
from unittest import TestCase
from bs4 import BeautifulSoup as bs
import re
from database_handler import input_file_parser, common_objects

aquapolis_compare = [
    ("Aipom", "aquapolis-aipom"),
    ("Ampharos", "aquapolis-ampharos"),
    ("Ampharos (H1)", "aquapolis-ampharos-h1"),
    ("Apricorn Forest", "aquapolis-apricorn-forest"),
    ("Arcanine", "aquapolis-arcanine"),
    ("Arcanine (H2)", "aquapolis-arcanine-h2"),
    ("Ariados", "aquapolis-ariados"),
    ("Ariados (H3)", "aquapolis-ariados-h3"),
    ("Azumarill", "aquapolis-azumarill"),
    ("Azumarill (H4)", "aquapolis-azumarill-h4"),
    ("Bellossom", "aquapolis-bellossom"),
    ("Bellossom (H5)", "aquapolis-bellossom-h5"),
    ("Bellsprout", "aquapolis-bellsprout-45"),
    ("Bellsprout", "aquapolis-bellsprout-68"),
    ("Blissey", "aquapolis-blissey"),
    ("Blissey (H6)", "aquapolis-blissey-h6"),
    ("Boost Energy", "aquapolis-boost-energy"),
    ("Chansey", "aquapolis-chansey"),
    ("Chinchou", "aquapolis-chinchou-70"),
    ("Chinchou", "aquapolis-chinchou-71"),
    ("Crystal Energy", "aquapolis-crystal-energy"),
    ("Cubone", "aquapolis-cubone"),
    ("Darkness Cube 01", "aquapolis-darkness-cube-01"),
    ("Darkness Energy", "aquapolis-darkness-energy"),
    ("Dodrio", "aquapolis-dodrio"),
    ("Doduo", "aquapolis-doduo"),
    ("Donphan", "aquapolis-donphan"),
    ("Drowzee (74a)", "aquapolis-drowzee-74a"),
    ("Drowzee (74b)", "aquapolis-drowzee-74b"),
    ("Eevee", "aquapolis-eevee"),
    ("Electrode", "aquapolis-electrode"),
    ("Electrode (H7)", "aquapolis-electrode-h7"),
    ("Elekid", "aquapolis-elekid"),
    ("Energy Switch", "aquapolis-energy-switch"),
    ("Entei", "aquapolis-entei"),
    ("Entei (H8)", "aquapolis-entei-h8"),
    ("Espeon", "aquapolis-espeon"),
    ("Espeon (H9)", "aquapolis-espeon-h9"),
    ("Exeggcute", "aquapolis-exeggcute-76"),
    ("Exeggcute", "aquapolis-exeggcute-77"),
    ("Exeggutor", "aquapolis-exeggutor-12"),
    ("Exeggutor", "aquapolis-exeggutor-13"),
    ("Exeggutor (H10)", "aquapolis-exeggutor-h10"),
    ("Fighting Cube 01", "aquapolis-fighting-cube-01"),
    ("Fire Cube 01", "aquapolis-fire-cube-01"),
    ("Flaaffy", "aquapolis-flaaffy"),
    ("Forest Guardian", "aquapolis-forest-guardian"),
    ("Furret", "aquapolis-furret"),
    ("Gloom", "aquapolis-gloom"),
    ("Goldeen", "aquapolis-goldeen"),
    ("Golduck (50a)", "aquapolis-golduck-50a"),
    ("Golduck (50b)", "aquapolis-golduck-50b"),
    ("Grass Cube 01", "aquapolis-grass-cube-01"),
    ("Grimer", "aquapolis-grimer"),
    ("Growlithe", "aquapolis-growlithe-51"),
    ("Growlithe", "aquapolis-growlithe-80"),
    ("Healing Berry", "aquapolis-healing-berry"),
    ("Hitmonchan", "aquapolis-hitmonchan"),
    ("Hitmontop", "aquapolis-hitmontop"),
    ("Hoppip", "aquapolis-hoppip"),
    ("Horsea", "aquapolis-horsea-84"),
    ("Horsea", "aquapolis-horsea-85"),
    ("Houndoom", "aquapolis-houndoom-14"),
    ("Houndoom", "aquapolis-houndoom-15"),
    ("Houndoom (H11)", "aquapolis-houndoom-h11"),
    ("Houndour", "aquapolis-houndour-86"),
    ("Houndour", "aquapolis-houndour-87"),
    ("Hypno", "aquapolis-hypno"),
    ("Hypno (H12)", "aquapolis-hypno-h12"),
    ("Juggler", "aquapolis-juggler"),
    ("Jumpluff", "aquapolis-jumpluff"),
    ("Jumpluff (H13)", "aquapolis-jumpluff-h13"),
    ("Jynx", "aquapolis-jynx"),
    ("Kangaskhan", "aquapolis-kangaskhan"),
    ("Kingdra", "aquapolis-kingdra-148"),
    ("Kingdra", "aquapolis-kingdra-19"),
    ("Kingdra (H14)", "aquapolis-kingdra-h14"),
    ("Lanturn", "aquapolis-lanturn-20"),
    ("Lanturn", "aquapolis-lanturn-21"),
    ("Lanturn (H15)", "aquapolis-lanturn-h15"),
    ("Larvitar", "aquapolis-larvitar"),
    ("Lickitung", "aquapolis-lickitung"),
    ("Lightning Cube 01", "aquapolis-lightning-cube-01"),
    ("Lugia", "aquapolis-lugia"),
    ("Magnemite", "aquapolis-magnemite-52"),
    ("Magnemite", "aquapolis-magnemite-91"),
    ("Magneton", "aquapolis-magneton"),
    ("Magneton (H16)", "aquapolis-magneton-h16"),
    ("Mankey", "aquapolis-mankey"),
    ("Mareep", "aquapolis-mareep"),
    ("Marill", "aquapolis-marill"),
    ("Marowak", "aquapolis-marowak"),
    ("Memory Berry", "aquapolis-memory-berry"),
    ("Metal Cube 01", "aquapolis-metal-cube-01"),
    ("Metal Energy", "aquapolis-metal-energy"),
    ("Miltank", "aquapolis-miltank"),
    ("Mr. Mime (95a)", "aquapolis-mr-mime-95a"),
    ("Mr. Mime (95b)", "aquapolis-mr-mime-95b"),
    ("Muk", "aquapolis-muk"),
    ("Muk (H17)", "aquapolis-muk-h17"),
    ("Nidoking", "aquapolis-nidoking-150"),
    ("Nidoking", "aquapolis-nidoking-24"),
    ("Nidoking (H18)", "aquapolis-nidoking-h18"),
    ("Nidoran M", "aquapolis-nidoran-m"),
    ("Nidorino", "aquapolis-nidorino"),
    ("Ninetales", "aquapolis-ninetales"),
    ("Ninetales (H19)", "aquapolis-ninetales-h19"),
    ("Octillery", "aquapolis-octillery"),
    ("Octillery (H20)", "aquapolis-octillery-h20"),
    ("Oddish", "aquapolis-oddish"),
    ("Onix", "aquapolis-onix"),
    ("Paras", "aquapolis-paras"),
    ("Parasect", "aquapolis-parasect"),
    ("Phanpy", "aquapolis-phanpy"),
    ("Pinsir", "aquapolis-pinsir"),
    ("Pokemon Fan Club", "aquapolis-pokemon-fan-club"),
    ("Pokemon Park", "aquapolis-pokemon-park"),
    ("Ponyta", "aquapolis-ponyta"),
    ("Porygon (103a)", "aquapolis-porygon-103a"),
    ("Porygon (103b)", "aquapolis-porygon-103b"),
    ("Porygon2", "aquapolis-porygon2"),
    ("Power Plant", "aquapolis-power-plant"),
    ("Primeape", "aquapolis-primeape"),
    ("Psychic Cube 01", "aquapolis-psychic-cube-01"),
    ("Psyduck", "aquapolis-psyduck"),
    ("Pupitar", "aquapolis-pupitar"),
    ("Quagsire", "aquapolis-quagsire"),
    ("Rainbow Energy", "aquapolis-rainbow-energy"),
    ("Rapidash", "aquapolis-rapidash"),
    ("Remoraid", "aquapolis-remoraid"),
    ("Scizor", "aquapolis-scizor"),
    ("Scizor (H21)", "aquapolis-scizor-h21"),
    ("Scyther", "aquapolis-scyther-106"),
    ("Scyther", "aquapolis-scyther-57"),
    ("Seadra", "aquapolis-seadra"),
    ("Seaking", "aquapolis-seaking"),
    ("Seer", "aquapolis-seer"),
    ("Sentret", "aquapolis-sentret"),
    ("Skiploom", "aquapolis-skiploom"),
    ("Slowbro", "aquapolis-slowbro"),
    ("Slowking", "aquapolis-slowking"),
    ("Slowking (H22)", "aquapolis-slowking-h22"),
    ("Slowpoke", "aquapolis-slowpoke"),
    ("Smeargle", "aquapolis-smeargle"),
    ("Smoochum", "aquapolis-smoochum"),
    ("Sneasel", "aquapolis-sneasel"),
    ("Spinarak", "aquapolis-spinarak-111"),
    ("Spinarak", "aquapolis-spinarak-62"),
    ("Steelix", "aquapolis-steelix"),
    ("Steelix (H23)", "aquapolis-steelix-h23"),
    ("Sudowoodo", "aquapolis-sudowoodo"),
    ("Sudowoodo (H24)", "aquapolis-sudowoodo-h24"),
    ("Suicune", "aquapolis-suicune"),
    ("Suicune (H25)", "aquapolis-suicune-h25"),
    ("Super Energy Removal 2", "aquapolis-super-energy-removal-2"),
    ("Tangela", "aquapolis-tangela"),
    ("Tentacool", "aquapolis-tentacool"),
    ("Tentacruel", "aquapolis-tentacruel"),
    ("Tentacruel (H26)", "aquapolis-tentacruel-h26"),
    ("Time Shard", "aquapolis-time-shard"),
    ("Togepi", "aquapolis-togepi"),
    ("Togetic", "aquapolis-togetic"),
    ("Togetic (H27)", "aquapolis-togetic-h27"),
    ("Town Volunteers", "aquapolis-town-volunteers"),
    ("Traveling Salesman", "aquapolis-traveling-salesman"),
    ("Tyranitar", "aquapolis-tyranitar"),
    ("Tyranitar (H28)", "aquapolis-tyranitar-h28"),
    ("Tyrogue", "aquapolis-tyrogue"),
    ("Umbreon", "aquapolis-umbreon"),
    ("Umbreon (H29)", "aquapolis-umbreon-h29"),
    ("Undersea Ruins", "aquapolis-undersea-ruins"),
    ("Victreebel", "aquapolis-victreebel"),
    ("Victreebel (H30)", "aquapolis-victreebel-h30"),
    ("Vileplume", "aquapolis-vileplume"),
    ("Vileplume (H31)", "aquapolis-vileplume-h31"),
    ("Voltorb", "aquapolis-voltorb-115"),
    ("Voltorb", "aquapolis-voltorb-64"),
    ("Vulpix", "aquapolis-vulpix"),
    ("Warp Energy", "aquapolis-warp-energy"),
    ("Water Cube 01", "aquapolis-water-cube-01"),
    ("Weakness Guard", "aquapolis-weakness-guard"),
    ("Weepinbell", "aquapolis-weepinbell"),
    ("Wooper", "aquapolis-wooper-117"),
    ("Wooper", "aquapolis-wooper-66"),
    ("Zapdos", "aquapolis-zapdos"),
    ("Zapdos (H32)", "aquapolis-zapdos-h32"),
]

aquapolis_set_list_compare = [
    {
        "card_name": "Ampharos",
        "card_type": "Lightning",
        "card_rarity": "Rare Holo",
        "card_index": 1,
        "card_class": "",
    },
    {
        "card_name": "Arcanine",
        "card_type": "Fire",
        "card_rarity": "Rare Holo",
        "card_index": 2,
        "card_class": "",
    },
    {
        "card_name": "Ariados",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 3,
        "card_class": "",
    },
    {
        "card_name": "Azumarill",
        "card_type": "Water",
        "card_rarity": "Rare Holo",
        "card_index": 4,
        "card_class": "",
    },
    {
        "card_name": "Bellossom",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 5,
        "card_class": "",
    },
    {
        "card_name": "Blissey",
        "card_type": "Colorless",
        "card_rarity": "Rare Holo",
        "card_index": 6,
        "card_class": "",
    },
    {
        "card_name": "Electrode",
        "card_type": "Lightning",
        "card_rarity": "Rare Holo",
        "card_index": 7,
        "card_class": "",
    },
    {
        "card_name": "Entei",
        "card_type": "Fire",
        "card_rarity": "Rare Holo",
        "card_index": 8,
        "card_class": "",
    },
    {
        "card_name": "Espeon",
        "card_type": "Psychic",
        "card_rarity": "Rare Holo",
        "card_index": 9,
        "card_class": "",
    },
    {
        "card_name": "Exeggutor",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 10,
        "card_class": "",
    },
    {
        "card_name": "Houndoom",
        "card_type": "Darkness",
        "card_rarity": "Rare Holo",
        "card_index": 11,
        "card_class": "",
    },
    {
        "card_name": "Hypno",
        "card_type": "Psychic",
        "card_rarity": "Rare Holo",
        "card_index": 12,
        "card_class": "",
    },
    {
        "card_name": "Jumpluff",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 13,
        "card_class": "",
    },
    {
        "card_name": "Kingdra",
        "card_type": "Water",
        "card_rarity": "Rare Holo",
        "card_index": 14,
        "card_class": "",
    },
    {
        "card_name": "Lanturn",
        "card_type": "Lightning",
        "card_rarity": "Rare Holo",
        "card_index": 15,
        "card_class": "",
    },
    {
        "card_name": "Magneton",
        "card_type": "Metal",
        "card_rarity": "Rare Holo",
        "card_index": 16,
        "card_class": "",
    },
    {
        "card_name": "Muk",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 17,
        "card_class": "",
    },
    {
        "card_name": "Nidoking",
        "card_type": "Fighting",
        "card_rarity": "Rare Holo",
        "card_index": 18,
        "card_class": "",
    },
    {
        "card_name": "Ninetales",
        "card_type": "Fire",
        "card_rarity": "Rare Holo",
        "card_index": 19,
        "card_class": "",
    },
    {
        "card_name": "Octillery",
        "card_type": "Water",
        "card_rarity": "Rare Holo",
        "card_index": 20,
        "card_class": "",
    },
    {
        "card_name": "Scizor",
        "card_type": "Metal",
        "card_rarity": "Rare Holo",
        "card_index": 21,
        "card_class": "",
    },
    {
        "card_name": "Slowking",
        "card_type": "Psychic",
        "card_rarity": "Rare Holo",
        "card_index": 22,
        "card_class": "",
    },
    {
        "card_name": "Steelix",
        "card_type": "Metal",
        "card_rarity": "Rare Holo",
        "card_index": 23,
        "card_class": "",
    },
    {
        "card_name": "Sudowoodo",
        "card_type": "Fighting",
        "card_rarity": "Rare Holo",
        "card_index": 24,
        "card_class": "",
    },
    {
        "card_name": "Suicune",
        "card_type": "Water",
        "card_rarity": "Rare Holo",
        "card_index": 25,
        "card_class": "",
    },
    {
        "card_name": "Tentacruel",
        "card_type": "Water",
        "card_rarity": "Rare Holo",
        "card_index": 26,
        "card_class": "",
    },
    {
        "card_name": "Togetic",
        "card_type": "Colorless",
        "card_rarity": "Rare Holo",
        "card_index": 27,
        "card_class": "",
    },
    {
        "card_name": "Tyranitar",
        "card_type": "Darkness",
        "card_rarity": "Rare Holo",
        "card_index": 28,
        "card_class": "",
    },
    {
        "card_name": "Umbreon",
        "card_type": "Darkness",
        "card_rarity": "Rare Holo",
        "card_index": 29,
        "card_class": "",
    },
    {
        "card_name": "Victreebel",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 30,
        "card_class": "",
    },
    {
        "card_name": "Vileplume",
        "card_type": "Grass",
        "card_rarity": "Rare Holo",
        "card_index": 31,
        "card_class": "",
    },
    {
        "card_name": "Zapdos",
        "card_type": "Lightning",
        "card_rarity": "Rare Holo",
        "card_index": 32,
        "card_class": "",
    },
    {
        "card_name": "Ampharos",
        "card_type": "Lightning",
        "card_rarity": "Rare",
        "card_index": 1,
        "card_class": "",
    },
    {
        "card_name": "Arcanine",
        "card_type": "Fire",
        "card_rarity": "Rare",
        "card_index": 2,
        "card_class": "",
    },
    {
        "card_name": "Ariados",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 3,
        "card_class": "",
    },
    {
        "card_name": "Azumarill",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 4,
        "card_class": "",
    },
    {
        "card_name": "Bellossom",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 5,
        "card_class": "",
    },
    {
        "card_name": "Blissey",
        "card_type": "Colorless",
        "card_rarity": "Rare",
        "card_index": 6,
        "card_class": "",
    },
    {
        "card_name": "Donphan",
        "card_type": "Fighting",
        "card_rarity": "Rare",
        "card_index": 7,
        "card_class": "",
    },
    {
        "card_name": "Electrode",
        "card_type": "Lightning",
        "card_rarity": "Rare",
        "card_index": 8,
        "card_class": "",
    },
    {
        "card_name": "Elekid",
        "card_type": "Lightning",
        "card_rarity": "Rare",
        "card_index": 9,
        "card_class": "",
    },
    {
        "card_name": "Entei",
        "card_type": "Fire",
        "card_rarity": "Rare",
        "card_index": 10,
        "card_class": "",
    },
    {
        "card_name": "Espeon",
        "card_type": "Psychic",
        "card_rarity": "Rare",
        "card_index": 11,
        "card_class": "",
    },
    {
        "card_name": "Exeggutor",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 12,
        "card_class": "",
    },
    {
        "card_name": "Exeggutor",
        "card_type": "Psychic",
        "card_rarity": "Rare",
        "card_index": 13,
        "card_class": "",
    },
    {
        "card_name": "Houndoom",
        "card_type": "Fire",
        "card_rarity": "Rare",
        "card_index": 14,
        "card_class": "",
    },
    {
        "card_name": "Houndoom",
        "card_type": "Darkness",
        "card_rarity": "Rare",
        "card_index": 15,
        "card_class": "",
    },
    {
        "card_name": "Hypno",
        "card_type": "Psychic",
        "card_rarity": "Rare",
        "card_index": 16,
        "card_class": "",
    },
    {
        "card_name": "Jumpluff",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 17,
        "card_class": "",
    },
    {
        "card_name": "Jynx",
        "card_type": "Psychic",
        "card_rarity": "Rare",
        "card_index": 18,
        "card_class": "",
    },
    {
        "card_name": "Kingdra",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 19,
        "card_class": "",
    },
    {
        "card_name": "Lanturn",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 20,
        "card_class": "",
    },
    {
        "card_name": "Lanturn",
        "card_type": "Lightning",
        "card_rarity": "Rare",
        "card_index": 21,
        "card_class": "",
    },
    {
        "card_name": "Magneton",
        "card_type": "Metal",
        "card_rarity": "Rare",
        "card_index": 22,
        "card_class": "",
    },
    {
        "card_name": "Muk",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 23,
        "card_class": "",
    },
    {
        "card_name": "Nidoking",
        "card_type": "Fighting",
        "card_rarity": "Rare",
        "card_index": 24,
        "card_class": "",
    },
    {
        "card_name": "Ninetales",
        "card_type": "Fire",
        "card_rarity": "Rare",
        "card_index": 25,
        "card_class": "",
    },
    {
        "card_name": "Octillery",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 26,
        "card_class": "",
    },
    {
        "card_name": "Parasect",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 27,
        "card_class": "",
    },
    {
        "card_name": "Porygon2",
        "card_type": "Colorless",
        "card_rarity": "Rare",
        "card_index": 28,
        "card_class": "",
    },
    {
        "card_name": "Primeape",
        "card_type": "Fighting",
        "card_rarity": "Rare",
        "card_index": 29,
        "card_class": "",
    },
    {
        "card_name": "Quagsire",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 30,
        "card_class": "",
    },
    {
        "card_name": "Rapidash",
        "card_type": "Fire",
        "card_rarity": "Rare",
        "card_index": 31,
        "card_class": "",
    },
    {
        "card_name": "Scizor",
        "card_type": "Metal",
        "card_rarity": "Rare",
        "card_index": 32,
        "card_class": "",
    },
    {
        "card_name": "Slowbro",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 33,
        "card_class": "",
    },
    {
        "card_name": "Slowking",
        "card_type": "Psychic",
        "card_rarity": "Rare",
        "card_index": 34,
        "card_class": "",
    },
    {
        "card_name": "Steelix",
        "card_type": "Metal",
        "card_rarity": "Rare",
        "card_index": 35,
        "card_class": "",
    },
    {
        "card_name": "Sudowoodo",
        "card_type": "Fighting",
        "card_rarity": "Rare",
        "card_index": 36,
        "card_class": "",
    },
    {
        "card_name": "Suicune",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 37,
        "card_class": "",
    },
    {
        "card_name": "Tentacruel",
        "card_type": "Water",
        "card_rarity": "Rare",
        "card_index": 38,
        "card_class": "",
    },
    {
        "card_name": "Togetic",
        "card_type": "Colorless",
        "card_rarity": "Rare",
        "card_index": 39,
        "card_class": "",
    },
    {
        "card_name": "Tyranitar",
        "card_type": "Darkness",
        "card_rarity": "Rare",
        "card_index": 40,
        "card_class": "",
    },
    {
        "card_name": "Umbreon",
        "card_type": "Darkness",
        "card_rarity": "Rare",
        "card_index": 41,
        "card_class": "",
    },
    {
        "card_name": "Victreebel",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 42,
        "card_class": "",
    },
    {
        "card_name": "Vileplume",
        "card_type": "Grass",
        "card_rarity": "Rare",
        "card_index": 43,
        "card_class": "",
    },
    {
        "card_name": "Zapdos",
        "card_type": "Lightning",
        "card_rarity": "Rare",
        "card_index": 44,
        "card_class": "",
    },
    {
        "card_name": "Bellsprout",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 45,
        "card_class": "",
    },
    {
        "card_name": "Dodrio",
        "card_type": "Colorless",
        "card_rarity": "Uncommon",
        "card_index": 46,
        "card_class": "",
    },
    {
        "card_name": "Flaaffy",
        "card_type": "Lightning",
        "card_rarity": "Uncommon",
        "card_index": 47,
        "card_class": "",
    },
    {
        "card_name": "Furret",
        "card_type": "Colorless",
        "card_rarity": "Uncommon",
        "card_index": 48,
        "card_class": "",
    },
    {
        "card_name": "Gloom",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 49,
        "card_class": "",
    },
    {
        "card_name": "Golduck",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 50,
        "card_class": "",
    },
    {
        "card_name": "Golduck",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 50,
        "card_class": "",
    },
    {
        "card_name": "Growlithe",
        "card_type": "Fire",
        "card_rarity": "Uncommon",
        "card_index": 51,
        "card_class": "",
    },
    {
        "card_name": "Magnemite",
        "card_type": "Metal",
        "card_rarity": "Uncommon",
        "card_index": 52,
        "card_class": "",
    },
    {
        "card_name": "Marill",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 53,
        "card_class": "",
    },
    {
        "card_name": "Marowak",
        "card_type": "Fighting",
        "card_rarity": "Uncommon",
        "card_index": 54,
        "card_class": "",
    },
    {
        "card_name": "Nidorino",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 55,
        "card_class": "",
    },
    {
        "card_name": "Pupitar",
        "card_type": "Fighting",
        "card_rarity": "Uncommon",
        "card_index": 56,
        "card_class": "",
    },
    {
        "card_name": "Scyther",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 57,
        "card_class": "",
    },
    {
        "card_name": "Seadra",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 58,
        "card_class": "",
    },
    {
        "card_name": "Seaking",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 59,
        "card_class": "",
    },
    {
        "card_name": "Skiploom",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 60,
        "card_class": "",
    },
    {
        "card_name": "Smoochum",
        "card_type": "Psychic",
        "card_rarity": "Uncommon",
        "card_index": 61,
        "card_class": "",
    },
    {
        "card_name": "Spinarak",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 62,
        "card_class": "",
    },
    {
        "card_name": "Tyrogue",
        "card_type": "Fighting",
        "card_rarity": "Uncommon",
        "card_index": 63,
        "card_class": "",
    },
    {
        "card_name": "Voltorb",
        "card_type": "Lightning",
        "card_rarity": "Uncommon",
        "card_index": 64,
        "card_class": "",
    },
    {
        "card_name": "Weepinbell",
        "card_type": "Grass",
        "card_rarity": "Uncommon",
        "card_index": 65,
        "card_class": "",
    },
    {
        "card_name": "Wooper",
        "card_type": "Water",
        "card_rarity": "Uncommon",
        "card_index": 66,
        "card_class": "",
    },
    {
        "card_name": "Aipom",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 67,
        "card_class": "",
    },
    {
        "card_name": "Bellsprout",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 68,
        "card_class": "",
    },
    {
        "card_name": "Chansey",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 69,
        "card_class": "",
    },
    {
        "card_name": "Chinchou",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 70,
        "card_class": "",
    },
    {
        "card_name": "Chinchou",
        "card_type": "Lightning",
        "card_rarity": "Common",
        "card_index": 71,
        "card_class": "",
    },
    {
        "card_name": "Cubone",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 72,
        "card_class": "",
    },
    {
        "card_name": "Doduo",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 73,
        "card_class": "",
    },
    {
        "card_name": "Drowzee",
        "card_type": "Psychic",
        "card_rarity": "Common",
        "card_index": 74,
        "card_class": "",
    },
    {
        "card_name": "Drowzee",
        "card_type": "Psychic",
        "card_rarity": "Common",
        "card_index": 74,
        "card_class": "",
    },
    {
        "card_name": "Eevee",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 75,
        "card_class": "",
    },
    {
        "card_name": "Exeggcute",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 76,
        "card_class": "",
    },
    {
        "card_name": "Exeggcute",
        "card_type": "Psychic",
        "card_rarity": "Common",
        "card_index": 77,
        "card_class": "",
    },
    {
        "card_name": "Goldeen",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 78,
        "card_class": "",
    },
    {
        "card_name": "Grimer",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 79,
        "card_class": "",
    },
    {
        "card_name": "Growlithe",
        "card_type": "Fire",
        "card_rarity": "Common",
        "card_index": 80,
        "card_class": "",
    },
    {
        "card_name": "Hitmonchan",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 81,
        "card_class": "",
    },
    {
        "card_name": "Hitmontop",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 82,
        "card_class": "",
    },
    {
        "card_name": "Hoppip",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 83,
        "card_class": "",
    },
    {
        "card_name": "Horsea",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 84,
        "card_class": "",
    },
    {
        "card_name": "Horsea",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 85,
        "card_class": "",
    },
    {
        "card_name": "Houndour",
        "card_type": "Fire",
        "card_rarity": "Common",
        "card_index": 86,
        "card_class": "",
    },
    {
        "card_name": "Houndour",
        "card_type": "Darkness",
        "card_rarity": "Common",
        "card_index": 87,
        "card_class": "",
    },
    {
        "card_name": "Kangaskhan",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 88,
        "card_class": "",
    },
    {
        "card_name": "Larvitar",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 89,
        "card_class": "",
    },
    {
        "card_name": "Lickitung",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 90,
        "card_class": "",
    },
    {
        "card_name": "Magnemite",
        "card_type": "Lightning",
        "card_rarity": "Common",
        "card_index": 91,
        "card_class": "",
    },
    {
        "card_name": "Mankey",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 92,
        "card_class": "",
    },
    {
        "card_name": "Mareep",
        "card_type": "Lightning",
        "card_rarity": "Common",
        "card_index": 93,
        "card_class": "",
    },
    {
        "card_name": "Miltank",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 94,
        "card_class": "",
    },
    {
        "card_name": "Mr. Mime",
        "card_type": "Psychic",
        "card_rarity": "Common",
        "card_index": 95,
        "card_class": "",
    },
    {
        "card_name": "Mr. Mime",
        "card_type": "Psychic",
        "card_rarity": "Common",
        "card_index": 95,
        "card_class": "",
    },
    {
        "card_name": "Nidoran M",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 96,
        "card_class": "",
    },
    {
        "card_name": "Oddish",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 97,
        "card_class": "",
    },
    {
        "card_name": "Onix",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 98,
        "card_class": "",
    },
    {
        "card_name": "Paras",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 99,
        "card_class": "",
    },
    {
        "card_name": "Phanpy",
        "card_type": "Fighting",
        "card_rarity": "Common",
        "card_index": 100,
        "card_class": "",
    },
    {
        "card_name": "Pinsir",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 101,
        "card_class": "",
    },
    {
        "card_name": "Ponyta",
        "card_type": "Fire",
        "card_rarity": "Common",
        "card_index": 102,
        "card_class": "",
    },
    {
        "card_name": "Porygon",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 103,
        "card_class": "",
    },
    {
        "card_name": "Porygon",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 103,
        "card_class": "",
    },
    {
        "card_name": "Psyduck",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 104,
        "card_class": "",
    },
    {
        "card_name": "Remoraid",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 105,
        "card_class": "",
    },
    {
        "card_name": "Scyther",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 106,
        "card_class": "",
    },
    {
        "card_name": "Sentret",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 107,
        "card_class": "",
    },
    {
        "card_name": "Slowpoke",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 108,
        "card_class": "",
    },
    {
        "card_name": "Smeargle",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 109,
        "card_class": "",
    },
    {
        "card_name": "Sneasel",
        "card_type": "Darkness",
        "card_rarity": "Common",
        "card_index": 110,
        "card_class": "",
    },
    {
        "card_name": "Spinarak",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 111,
        "card_class": "",
    },
    {
        "card_name": "Tangela",
        "card_type": "Grass",
        "card_rarity": "Common",
        "card_index": 112,
        "card_class": "",
    },
    {
        "card_name": "Tentacool",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 113,
        "card_class": "",
    },
    {
        "card_name": "Togepi",
        "card_type": "Colorless",
        "card_rarity": "Common",
        "card_index": 114,
        "card_class": "",
    },
    {
        "card_name": "Voltorb",
        "card_type": "Lightning",
        "card_rarity": "Common",
        "card_index": 115,
        "card_class": "",
    },
    {
        "card_name": "Vulpix",
        "card_type": "Fire",
        "card_rarity": "Common",
        "card_index": 116,
        "card_class": "",
    },
    {
        "card_name": "Wooper",
        "card_type": "Water",
        "card_rarity": "Common",
        "card_index": 117,
        "card_class": "",
    },
    {
        "card_name": "Apricorn Forest",
        "card_type": "Stadium",
        "card_rarity": "Rare",
        "card_index": 118,
        "card_class": "",
    },
    {
        "card_name": "Darkness Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 119,
        "card_class": "",
    },
    {
        "card_name": "Energy Switch",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 120,
        "card_class": "",
    },
    {
        "card_name": "Fighting Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 121,
        "card_class": "",
    },
    {
        "card_name": "Fire Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 122,
        "card_class": "",
    },
    {
        "card_name": "Forest Guardian",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 123,
        "card_class": "",
    },
    {
        "card_name": "Grass Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 124,
        "card_class": "",
    },
    {
        "card_name": "Healing Berry",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 125,
        "card_class": "",
    },
    {
        "card_name": "Juggler",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 126,
        "card_class": "",
    },
    {
        "card_name": "Lightning Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 127,
        "card_class": "",
    },
    {
        "card_name": "Memory Berry",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 128,
        "card_class": "",
    },
    {
        "card_name": "Metal Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 129,
        "card_class": "",
    },
    {
        "card_name": "Pokemon Fan Club",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 130,
        "card_class": "",
    },
    {
        "card_name": "Pokemon Park",
        "card_type": "Stadium",
        "card_rarity": "Uncommon",
        "card_index": 131,
        "card_class": "",
    },
    {
        "card_name": "Psychic Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 132,
        "card_class": "",
    },
    {
        "card_name": "Seer",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 133,
        "card_class": "",
    },
    {
        "card_name": "Super Energy Removal 2",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 134,
        "card_class": "",
    },
    {
        "card_name": "Time Shard",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 135,
        "card_class": "",
    },
    {
        "card_name": "Town Volunteers",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 136,
        "card_class": "",
    },
    {
        "card_name": "Traveling Salesman",
        "card_type": "Support",
        "card_rarity": "Uncommon",
        "card_index": 137,
        "card_class": "",
    },
    {
        "card_name": "Undersea Ruins",
        "card_type": "Stadium",
        "card_rarity": "Uncommon",
        "card_index": 138,
        "card_class": "",
    },
    {
        "card_name": "Power Plant",
        "card_type": "Stadium",
        "card_rarity": "Uncommon",
        "card_index": 139,
        "card_class": "",
    },
    {
        "card_name": "Water Cube 01",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 140,
        "card_class": "",
    },
    {
        "card_name": "Weakness Guard",
        "card_type": "Trainer",
        "card_rarity": "Uncommon",
        "card_index": 141,
        "card_class": "",
    },
    {
        "card_name": "Darkness Energy",
        "card_type": "Darkness",
        "card_rarity": "Rare",
        "card_index": 142,
        "card_class": "",
    },
    {
        "card_name": "Metal Energy",
        "card_type": "Metal",
        "card_rarity": "Rare",
        "card_index": 143,
        "card_class": "",
    },
    {
        "card_name": "Rainbow Energy",
        "card_type": "Rainbow",
        "card_rarity": "Rare",
        "card_index": 144,
        "card_class": "",
    },
    {
        "card_name": "Boost Energy",
        "card_type": "Colorless",
        "card_rarity": "Uncommon",
        "card_index": 145,
        "card_class": "",
    },
    {
        "card_name": "Crystal Energy",
        "card_type": "Colorless",
        "card_rarity": "Uncommon",
        "card_index": 146,
        "card_class": "",
    },
    {
        "card_name": "Warp Energy",
        "card_type": "Colorless",
        "card_rarity": "Uncommon",
        "card_index": 147,
        "card_class": "",
    },
    {
        "card_name": "Kingdra",
        "card_type": "Colorless",
        "card_rarity": "Rare Holo",
        "card_index": 148,
        "card_class": "",
    },
    {
        "card_name": "Lugia",
        "card_type": "Colorless",
        "card_rarity": "Rare Holo",
        "card_index": 149,
        "card_class": "",
    },
    {
        "card_name": "Nidoking",
        "card_type": "Colorless",
        "card_rarity": "Rare Holo",
        "card_index": 150,
        "card_class": "",
    },
]


class TestSetHtmlsSetup(TestCase):
    DATA_PATH = "../data_files/"

    def setUp(self) -> None:
        pass
        # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")

        # __init__.patch_get_file_hash(self)
        # __init__.patch_get_ffmpeg_metadata(self)
        # __init__.patch_move_media_file(self)
        # __init__.patch_extract_subclip(self)
        # __init__.patch_update_processed_file(self)

    def load_set_data_count(self, count):
        set_data_list = []
        for set_data in input_file_parser.load_set_data_dir(self.DATA_PATH):
            set_data_list.append(set_data)
            if len(set_data_list) == count:
                break
        return set_data_list


class TestSetHtmls(TestSetHtmlsSetup):
    #
    # def test_parse_set_codes(self):
    #     set_codes = input_file_parser.parse_set_codes()
    #     print(set_codes)
    #
    # # def test_setup_new_media_metadata(self):
    #
    # # with DBCreator(DBType.MEMORY) as db_setter_connection:
    # #     db_setter_connection.create_db()
    #
    # # if media_path_data := config_file_handler.load_json_file_content().get("media_folders"):
    # #     for media_path in media_path_data:
    # #         # print(media_path)
    # #         db_setter_connection.setup_media_directory(media_path)
    # def test_parse_set_data(self):
    #     set_codes = input_file_parser.parse_set_data()
    #     print(set_codes)

    def test_load_xy_primal_clash(self):
        set_name = "XY - Primal Clash"
        set_data_list = input_file_parser.load_set_data(self.DATA_PATH, set_name)
        for card in set_data_list.card_dict.values():
            print(card.to_dict())

    def test_load_aquapolis_set_htmls(self):
        set_data_list = self.load_set_data_count(1)
        assert type(set_data_list) is list
        assert len(set_data_list) == 1
        set_data = set_data_list[0]
        assert len(set_data) == 186
        print(set_data)
        for index, card_key in enumerate(set_data):
            card_value = set_data[card_key]
            compare_value = aquapolis_compare[index]
            print(
                f"('{card_value[common_objects.CARD_NAME_COLUMN]}', '{card_value[common_objects.TCGP_PATH_COLUMN]}', '{card_value[common_objects.CARD_RARITY_COLUMN]}'),"
            )
            assert type(card_key) is int
            assert common_objects.OWN_COUNT_COLUMN in card_value
            assert type(card_value[common_objects.OWN_COUNT_COLUMN]) is int
            assert common_objects.STATE_WANT_COLUMN in card_value
            assert type(card_value[common_objects.STATE_WANT_COLUMN]) is int
            assert common_objects.CARD_NAME_COLUMN in card_value
            assert type(card_value[common_objects.CARD_NAME_COLUMN]) is str
            assert card_value[common_objects.CARD_NAME_COLUMN] == compare_value[0]
            assert common_objects.SET_NAME_COLUMN in card_value
            assert type(card_value[common_objects.SET_NAME_COLUMN]) is str
            assert card_value[common_objects.SET_INDEX_COLUMN] == 14
            assert card_value[common_objects.SET_NAME_COLUMN] == "Aquapolis"
            assert common_objects.PRICE_COLUMN in card_value
            assert type(card_value[common_objects.PRICE_COLUMN]) is float
            assert common_objects.CARD_RARITY_COLUMN in card_value
            assert common_objects.CARD_INDEX_COLUMN in card_value
            assert common_objects.STATE_GIFT_COLUMN in card_value
            assert common_objects.TCGP_ID_COLUMN in card_value
            assert type(card_value[common_objects.TCGP_ID_COLUMN]) is int
            assert common_objects.TCGP_PATH_COLUMN in card_value
            assert type(card_value[common_objects.TCGP_PATH_COLUMN]) is str
            assert card_value[common_objects.TCGP_PATH_COLUMN] == compare_value[1]

        # set_data = list(input_file_parser.load_set_data(self.DATA_PATH))
        # print(set_data)


class TestSetListHtmlsSetup(TestCase):
    SET_LIST_PATH = "../data_files/"

    def setUp(self) -> None:
        pass
        # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")

        # __init__.patch_get_file_hash(self)
        # __init__.patch_get_ffmpeg_metadata(self)
        # __init__.patch_move_media_file(self)
        # __init__.patch_extract_subclip(self)
        # __init__.patch_update_processed_file(self)

    def load_set_data_count(self, count):
        set_data_list = []
        for set_data in input_file_parser.load_set_list_data_dir(self.SET_LIST_PATH):
            set_data_list.append(set_data)
            if len(set_data_list) == count:
                break
        return set_data_list

    def load_all(self):
        return list(input_file_parser.load_set_list_data_dir(self.SET_LIST_PATH))


class TestSetListHtmls(TestSetListHtmlsSetup):

    def test_load_named_file_aquapolis_set_list_htmls(self):
        set_name = "Aquapolis"
        set_card_list = input_file_parser.load_set_list_from_name(
            self.SET_LIST_PATH, set_name
        )
        # f"{self.SET_LIST_PATH}{set_name}.html"
        # )
        for index, card in enumerate(set_card_list.card_list):
            print(f"{card.to_dict()},")
            # print(card.to_dict(), aquapolis_set_list_compare[index])
            # assert card.to_dict() == aquapolis_set_list_compare[index]
        assert aquapolis_set_list_compare == set_card_list.to_dict()
        # print(set_card_list)

    def test_load_aquapolis_set_list_htmls(self):
        set_data_list = self.load_set_data_count(1)
        assert type(set_data_list) is list
        assert len(set_data_list) == 1
        set_data = set_data_list[0]
        # print(len(set_data.card_list))
        assert len(set_data.card_list) == 186
        print(set_data)
        assert aquapolis_set_list_compare == set_data.to_dict()

        # for set_name in common_objects.get_set_name_list():
        #     print(set_name)

    def test_load_all_set_list_htmls(self):
        set_lists = self.load_all()
        assert len(set_lists) == len(common_objects.get_set_name_list())
        for set_list in set_lists:

            # print(set_list.set_name, len(set_list.card_list))
            broken_indices = set_list.get_broken_indices()
            card_rarities = set_list.get_rarities()
            card_types = set_list.get_types()
            if "" in card_types:
                print("Set Name: ", set_list.set_name)
                print("Set Types: ", set_list.get_types())
                print("Set Rarities: ", card_rarities)
                print("Set indexes: ", broken_indices)
            # print(len(set_list))


#
# class TestLoadAllSetup(TestCase):
#     SET_PATH = "../data_files/set_htmls/"
#     SET_LIST_PATH = "../data_files/set_list_htmls/"
#
#     def setUp(self) -> None:
#         pass
#         # self.media_directory_info = config_file_handler.load_json_file_content().get("media_folders")
#
#         # __init__.patch_get_file_hash(self)
#         # __init__.patch_get_ffmpeg_metadata(self)
#         # __init__.patch_move_media_file(self)
#         # __init__.patch_extract_subclip(self)
#         # __init__.patch_update_processed_file(self)
#
#     def load_set_data_count(self, count):
#         set_data_list = []
#         for set_data in input_file_parser.load_set_data_dir(self.SET_PATH):
#             set_data_list.append(set_data)
#             if len(set_data_list) == count:
#                 break
#         return set_data_list
#
#     def load_all_set(self):
#         return list(input_file_parser.load_set_data_dir(self.SET_PATH))
#
#     def load_set_list_data_count(self, count):
#         set_data_list = []
#         for set_data in input_file_parser.load_set_list_data_dir(self.SET_LIST_PATH):
#             set_data_list.append(set_data)
#             if len(set_data_list) == count:
#                 break
#         return set_data_list
#
#     def load_all_set_list(self):
#         return list(input_file_parser.load_set_list_data_dir(self.SET_LIST_PATH))
#
#
# class TestLoadAll(TestLoadAllSetup):
#     def test_combine_data_collection(self):
#         for set_data in self.load_all_set():
#             print(set_data)
