import requests

pokemon_category = "3"

r = requests.get(f"https://tcgcsv.com/tcgplayer/{pokemon_category}/groups")
all_groups = r.json()["results"]

for group in all_groups:
    group_id = group["groupId"]
    print(group)
    r = requests.get(
        f"https://tcgcsv.com/tcgplayer/{pokemon_category}/{group_id}/products"
    )
    products = r.json()["results"]

    for product in products:
        if "extendedData" in product:
            for extended_data in product["extendedData"]:
                if "Card Number" in extended_data.values():
                    print(f"Set: {group['name']}, Card Name: {product['name']}")
                    # print(product)
                    input()
        # Process product information
        # print(f"{product['productId']} - {product['name']}")
