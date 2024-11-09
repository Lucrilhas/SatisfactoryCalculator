import os
import requests
from bs4 import BeautifulSoup
from utils import *
import pandas as pd


def extract_items(items_container):
    items = []
    for item_data in items_container.contents[0].children:
        try:
            item_per_craft = item_data.contents[0].text.replace("×", "").strip()
            item_name = item_data.contents[2].text.strip()
            if "/wiki/" + item_name.replace(" ", "_") in blacklist_items:
                return None
            item_per_min = item_data.contents[3].text.replace("/", "").replace("min", "").strip()
            items.append({"item_name": item_name, "item_per_min": item_per_min})
        except (IndexError, AttributeError):
            logger.critical(f"Warning: Unexpected structure in item data: {item_data}")
            # items.append({'item_name': None, 'item_per_min': None})

    return items


def scrape_wiki_item_crafing(url: str) -> dict:
    # logger.info(url)
    response = requests.get(url)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, "html.parser")

    trs = soup.find("h3", string="Crafting").find_next_sibling("table").find("tbody").find_all("tr")
    trs.pop(0)

    crafts = {}
    for i, tr in enumerate(trs):
        tds = tr.find_all("td")
        recipe = tds[0].text.strip()
        ings = tds[1]
        produced_in = tds[2].find("a").text
        prods = tds[3]

        alt = "Alternate" in recipe
        if alt:
            recipe = recipe.replace("Alternate", "")
        asBy = "As byproduct" in recipe
        if asBy:
            recipe = recipe.replace("As byproduct", "")
        recipe = recipe.strip()

        ingredients = extract_items(ings)
        if not ingredients is None:
            crafts[recipe] = {
                "alternate": alt,
                "byproduct": asBy,
                "ingredients": ingredients,
                "produced_in": produced_in,
                "products": extract_items(prods),
            }

    return crafts


def get_recipes_data():
    os.makedirs(r"imgs", exist_ok=True)

    df = pd.read_csv(r"data/items.csv")
    # print(df)

    recipes = []
    for row in df.itertuples():
        if row.is_primary:
            logger.info(row.item)
        else:
            crafts = scrape_wiki_item_crafing(row.link)
            for recipe in crafts:
                if recipe in blacklist_recipes:
                    logger.warning(f"{row.item}  ---  {recipe}")
                    continue
                
                logger.info(f"{row.item}  ---  {recipe}")
                aux = {
                    "recipe": recipe,
                    "ingredient 0": None,
                    "ingredient 0 p_min": None,
                    "ingredient 1": None,
                    "ingredient 1 p_min": None,
                    "ingredient 2": None,
                    "ingredient 2 p_min": None,
                    "ingredient 3": None,
                    "ingredient 3 p_min": None,
                    "product": None,
                    "product p_min": None,
                    "by_product": None,
                    "by_product p_min": None,
                    "is_alternate": crafts[recipe]["alternate"],
                    "produced_in": crafts[recipe]["produced_in"],
                }
                for i, ing in enumerate(crafts[recipe]['ingredients']):
                    aux[f"ingredient {i}"] = ing.get("item_name")
                    aux[f"ingredient {i} p_min"] = ing.get("item_per_min")
                    
                for i, prod in enumerate(crafts[recipe]['products']):
                    if i == 0:
                        aux[f"product"] = prod.get("item_name")
                        aux[f"product p_min"] = prod.get("item_per_min")
                    elif i == 1:
                        aux[f"by_product"] = prod.get("item_name")
                        aux[f"by_product p_min"] = prod.get("item_per_min")
                recipes.append(aux)
                    
    recipes = pd.DataFrame(recipes)
    recipes.to_csv("data/recipes.csv", index=False)
