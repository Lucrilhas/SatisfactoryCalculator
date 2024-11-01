import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import logger
import json


def scrape_wiki_all_items(url: str) -> list[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        # logger.debug(response)
        soup = BeautifulSoup(response.content, "html.parser")

        return [i["href"] for i in soup.select("#mw-pages ul li a")]

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
    except Exception as e:  # Catch other potential exceptions during parsing
        logger.error(f"An error occurred during parsing: {e}")
        return None


def extract_items(items_container):
    items = []
    for item_data in items_container.contents[0].children:
        try:
            item_per_craft = item_data.contents[0].text.replace("×", "").strip()
            item_name = item_data.contents[2].text.strip()
            item_per_min = item_data.contents[3].text.replace("/", "").replace("min", "").strip()
            items.append({"item_name": item_name, "item_per_min": item_per_min})
        except (IndexError, AttributeError):
            logger.critical(f"Warning: Unexpected structure in item data: {item_data}")
            # items.append({'item_name': None, 'item_per_min': None})

    return items


def scrape_wiki_item_crafing(url: str) -> dict:
    logger.info(url)
    response = requests.get(url)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, "html.parser")

    trs = soup.find("h3", string="Crafting").find_next_sibling("table").find("tbody").find_all("tr")
    if trs is None:
        return None

    trs.pop(0)

    crafts = {}
    for i, tr in enumerate(trs):
        tds = tr.find_all("td")
        recipe = tds[0].text.strip()
        ings = tds[1]
        produced_in = tds[2].find("a").text
        prods = tds[3]

        # logger.info(f"recipe: {recipe}")
        # logger.info(f"produced_in: {produced_in}")
        alt = "Alternate" in recipe
        if alt:
            recipe = recipe[:-9]

        crafts[recipe] = {
            "alternate": alt,
            "ingredients": extract_items(ings),
            "produced_in": produced_in,
            "products": extract_items(prods),
        }

    return crafts


if __name__ == "__main__":
    load_dotenv()
    all_itens_url = os.getenv("MAIN_PAGE") + os.getenv("ALL_ITENS_PAGE")
    logger.info(all_itens_url)
    items_links = scrape_wiki_all_items(all_itens_url)

    if items_links:
        # for i in items_links:
        #     print(i)
        # recipe_data = scrape_wiki_item_crafing(os.getenv("MAIN_PAGE") + items_links[6])

        # recipe_data = scrape_wiki_item_crafing(os.getenv("MAIN_PAGE") + items_links[1])
        recipe_data = scrape_wiki_item_crafing(os.getenv("MAIN_PAGE") + items_links[2])
        print(json.dumps(recipe_data, sort_keys=False, indent=4))
