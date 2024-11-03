import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import *
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

        crafts[recipe] = {
            "alternate": alt,
            "byproduct": asBy,
            "ingredients": extract_items(ings),
            "produced_in": produced_in,
            "products": extract_items(prods),
        }

    return crafts


def scrape_title_img_item(url:str, main_page_link:str) -> str:
    # logger.info(url)
    response = requests.get(url)
    response.raise_for_status()
    # logger.debug(response)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find('span', class_='mw-page-title-main').text
    img_url = soup.find('img', class_='pi-image-thumbnail').get('src')
    img_url = main_page_link + img_url

    # logger.info(title)
    # logger.info(img_url)

    filename = os.path.join(r"data/imgs/" + title + r".png")
    response = requests.get(img_url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return title

if __name__ == "__main__":
    os.makedirs(r"data", exist_ok=True)
    os.makedirs(r"data/imgs", exist_ok=True)
    
    load_dotenv()
    main_page_link = os.getenv("MAIN_PAGE")
    all_itens_url = main_page_link + os.getenv("ALL_ITENS_PAGE")
    logger.info(all_itens_url)
    items_links = scrape_wiki_all_items(all_itens_url)

    if items_links:
        all_crafts = {}
        for indc, item_link in enumerate(items_links):
            item_name = item_link[6:]
            if item_name in primary_itens:
                logger.warning(item_name)
                title = scrape_title_img_item(main_page_link + item_link, main_page_link)
                img_path = r"data/imgs/" + title + r".png"
                color = get_main_color(img_path)
                all_crafts[title] = {'primary':True, 'hex_color': color}
                
            elif item_name in blacklist:
                logger.error(item_name)
            else:
                logger.debug(item_name)
                title = scrape_title_img_item(main_page_link + item_link, main_page_link)
                img_path = r"data/imgs/" + title + r".png"
                color = get_main_color(img_path)
                all_crafts[title] = {'recipes': scrape_wiki_item_crafing(main_page_link + item_link), 'primary':False, 'hex_color': color}

        with open(r'data/recipes.json', 'w') as f:
            json.dump(all_crafts, f, indent=4)
