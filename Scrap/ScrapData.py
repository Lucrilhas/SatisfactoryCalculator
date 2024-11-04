import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import *
import json

def extract_items(items_container):
    items = []
    for item_data in items_container.contents[0].children:
        try:
            item_per_craft = item_data.contents[0].text.replace("×", "").strip()
            item_name = item_data.contents[2].text.strip()
            if "/wiki/" + item_name.replace(' ', '_') in blacklist:
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
            recipe = recipe[:-9]
        asBy = "As byproduct" in recipe
        if asBy:
            recipe = recipe[:-13]

        
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

def scrape_image(name:str, item_link:str, main_page_link:str) -> str:
    # logger.info(url)
    response = requests.get(main_page_link + item_link)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, "html.parser")

    img_url = soup.find('img', class_='pi-image-thumbnail').get('src')
    img_url = main_page_link + img_url

    filepath = os.path.join(r"imgs/" + name + r".png")
    response = requests.get(img_url, stream=True)
    response.raise_for_status()
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath


def get_links_data():
    os.makedirs(r"imgs", exist_ok=True)
    
    load_dotenv()
    main_page_link = os.getenv("MAIN_PAGE")
    itens = read_json(r"jsons\itens_links.json")

    primary_items = (
        "/wiki/Bacon_Agaric",
        "/wiki/Bauxite",
        "/wiki/Beryl_Nut",
        "/wiki/Caterium_Ore",
        "/wiki/Coal",
        "/wiki/Copper_Ore",
        "/wiki/Crude_Oil",
        "/wiki/Excited_Photonic_Matter",
        "/wiki/Iron_Ore",
        "/wiki/Leaves",
        "/wiki/Limestone",
        "/wiki/Mycelia",
        "/wiki/Nitrogen_Gas",
        "/wiki/Paleberry",
        "/wiki/Raw_Quartz",
        "/wiki/SAM",
        "/wiki/Sulfur",
        "/wiki/Water"
        "/wiki/Wood",
    )

    all_crafts = {}
    for key in itens:
        link = itens.get(key).get('link')
        image_filepath = scrape_image(key, link, main_page_link)
        color = get_main_color(image_filepath)
        
        if link in primary_items:
            logger.warning(key)
            all_crafts[key] = {'primary':True, 'hex_color': color}
        else:
            logger.debug(key)
            all_crafts[key] = {'recipes': scrape_wiki_item_crafing(main_page_link + link), 'primary':False, 'hex_color': color}
            
    with open(r'jsons/recipes.json', 'w') as f:
        json.dump(all_crafts, f, indent=4)