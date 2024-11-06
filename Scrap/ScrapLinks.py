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
    except Exception as e:
        logger.error(f"An error occurred during parsing: {e}")
        return None


def save_all_links():
    os.makedirs(r"jsons", exist_ok=True)
    load_dotenv()
    main_page_link = os.getenv("MAIN_PAGE")
    all_itens_url = main_page_link + os.getenv("ALL_ITENS_PAGE")
    all_fuilds_url = main_page_link + os.getenv("ALL_FLUIDS_PAGE")
    logger.info([all_itens_url, all_fuilds_url])
    items_links = scrape_wiki_all_items(all_itens_url)
    fluid_links = scrape_wiki_all_items(all_fuilds_url)
    if items_links is None or fluid_links is None:
        return None
    links = set(items_links + fluid_links)
    
    
    links = [link for link in links if link not in blacklist_items]
    links.sort()

    links = {l.replace('_', ' ').replace('/wiki/', ''): {'link': l} for l in links}

    with open(r'jsons/itens_links.json', 'w') as f:
        json.dump(links, f, indent=4)
