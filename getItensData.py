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
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return [i["href"] for i in soup.select("#mw-pages ul li a")]

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
    except Exception as e:  # Catch other potential exceptions during parsing
        logger.error(f"An error occurred during parsing: {e}")
        return None

def scrape_wiki_item_tables(url:str) -> dict:
    logger.info(url)
    response = requests.get(url)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, 'html.parser')
    recipe_tables = soup.find_all('table', class_='wikitable sortable recipetable')

    recipe_data = []

    for table in recipe_tables:
        for row in table.find_all('tr')[1:]:  # Skip header row
            cells = row.find_all('td')
            if len(cells) >= 5: #Ensure all expected cells are present

                name = cells[0].get_text(strip=True)

                ingredients = []
                for item in cells[1].find_all('div', class_='recipe-item'):
                    amount = item.find('span', class_='item-amount').get_text(strip=True).replace('×','')
                    ingredient_name = item.find('span', class_='item-name').get_text(strip=True)
                    try:
                        ingredients.append((ingredient_name, int(amount)))
                    except ValueError: #Handle cases like "X ml" where amount is not a simple integer
                        ingredients.append((ingredient_name, amount))

                produced_in = cells[2].get_text(strip=True).replace('\n',', ')

                products = []
                for item in cells[3].find_all('div', class_='recipe-item'):
                   amount = item.find('span', class_='item-amount').get_text(strip=True).replace('×','')
                   product_name = item.find('span', class_='item-name').get_text(strip=True)
                   try:
                      products.append((product_name, int(amount)))
                   except ValueError:
                       products.append((product_name,amount))
                
                unlocked_by = cells[4].get_text(strip=True).replace('\n', ', ')


                recipe_data.append({
                    "name": name,
                    "ingredients": ingredients,
                    "produced_in": produced_in,
                    "products": products,
                    "unlocked_by": unlocked_by
                })

    return recipe_data


def extract_items(items_container):
    items = []
    for item_data in items_container.contents[0].children:
        try:
            item_per_craft = item_data.contents[0].text.replace("×", "").strip()
            item_name = item_data.contents[2].text.strip()
            item_per_min = item_data.contents[3].text.replace("/", "").replace("min", "").strip()
            items.append({'item_name': item_name, 'item_per_min': item_per_min})
        except (IndexError, AttributeError):
            # Handle cases where the expected structure is missing
            print(f"Warning: Unexpected structure in item data: {item_data}")  # Log the error for debugging.
            items.append({'item_name': None, 'item_per_min': None}) # or raise an exception, depending on your error handling strategy.

    return items


def scrape_wiki_item_crafing(url:str) -> dict:
    logger.info(url)
    response = requests.get(url)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, 'html.parser')

    trs = soup.find('h3', string="Crafting").find_next_sibling('table').find('tbody').find_all('tr')
    if trs is None:
        return None
    
    trs.pop(0)
    
    crafts = {}
    for i, tr in enumerate(trs):
        tds = tr.find_all('td')
        recipe = tds[0].text.strip()
        ings = tds[1]
        produced_in = tds[2].find('a').text
        prods = tds[3]

        # logger.info(f"recipe: {recipe}")
        # logger.info(f"produced_in: {produced_in}")
        alt = "Alternate" in recipe
        if alt:
            recipe = recipe[:-9]
            
        crafts[recipe] = {
            'alternate': alt,
            'ingredients': extract_items(ings),
            'produced_in': produced_in,
            'products': extract_items(prods),
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