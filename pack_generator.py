import random

from database_handler import common_objects


class Pack:
    def __init__(self, cards):
        self.cards = cards

    def open(self):
        pulled_cards = [None] * 10  # Initialize a list of 11 None values

        # 1. Commons (4)
        commons = [
            card
            for card in self.cards
            if card["card_rarity"] == "Common"
            and card["card_class"] in ["creature", "trainer"]
        ]
        if len(commons) >= 4:
            pulled_cards[0:4] = random.sample(commons, 4)

        # 2. Uncommons (3)
        uncommons = [
            card
            for card in self.cards
            if card["card_rarity"] == "Uncommon"
            and card["card_class"] in ["creature", "trainer"]
        ]
        if len(uncommons) >= 3:
            pulled_cards[4:7] = random.sample(uncommons, 3)

        # 3. Rares or Higher (1) - Weighted selection
        rare_or_higher_cards = [
            card
            for card in self.cards
            if card["card_rarity"] in common_objects.rare_sub_types.keys()
            and card["card_class"] in ["creature", "trainer"]
        ]

        # if not rare_or_higher_cards:
        #     raise ValueError("No rare or higher candidates found in card data.")
        if rare_or_higher_cards:
            # Weighted random selection for the rare or higher card
            cumulative_weights = [0] * len(rare_or_higher_cards)
            for i, card in enumerate(rare_or_higher_cards):
                cumulative_weights[i] = (
                    cumulative_weights[i - 1] if i > 0 else 0
                ) + common_objects.rare_sub_types[card["card_rarity"]]

            rand_num = random.random()
            for i, card in enumerate(rare_or_higher_cards):
                # print(card)
                if rand_num < cumulative_weights[i]:
                    pulled_cards[7] = (
                        card  # Place the selected card in the correct slot
                    )
                    break

        common_to_rare_cards = [
            card
            for card in self.cards
            if card["card_rarity"] in common_objects.card_rarities.keys()
            and card["card_class"] in ["creature", "trainer"]
            and card != pulled_cards[7]
        ]
        # 3. Rares or Higher (2) - Random selection from the remaining rare or higher cards
        if common_to_rare_cards:
            if pulled_cards[7]:
                pulled_cards[8:9] = random.sample(common_to_rare_cards, 1)
            else:
                pulled_cards[7:9] = random.sample(common_to_rare_cards, 2)

        # 4. Energy Card (1)
        energy_cards = [card for card in self.cards if card["card_class"] == "energy"]
        if energy_cards:
            pulled_cards[9] = random.choice(energy_cards)

        # 5. Reverse Foil (1 Common or Uncommon, can be any position except energy)
        reverse_foil_candidates = [
            card
            for card in pulled_cards
            if card
            and card["card_rarity"] in ("Common", "Uncommon", "Rare")
            and card["card_class"] in ["creature", "trainer"]
        ]
        for card in pulled_cards:
            if card and "Holo" in card["card_rarity"]:
                card["foil_type"] = "Holo"  # Set the foil type
        if reverse_foil_candidates:
            for card in reverse_foil_candidates:
                card["foil_type"] = "Holo"  # Set the foil type
            reverse_foil = random.choice(reverse_foil_candidates)
            reverse_foil["foil_type"] = "Reverse Holo"  # Set the foil type

        return pulled_cards
