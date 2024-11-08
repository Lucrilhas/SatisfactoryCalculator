import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import *
import json
import pandas as pd


def scrape_wiki_all_items(url: str) -> list[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        # logger.debug(response)
        soup = BeautifulSoup(response.content, "html.parser")

        return [i["title"] for i in soup.select("#mw-pages ul li a")]

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred during parsing: {e}")
        return None


def get_items_links():
    os.makedirs(r"data", exist_ok=True)
    logger.info([items_page_link, fluids_page_link])
    all_items = scrape_wiki_all_items(items_page_link) + scrape_wiki_all_items(fluids_page_link)

    items = [item for item in all_items if item not in blacklist_items]
    df = pd.DataFrame(items, columns=['item'])
    df['link'] = main_page_link + "/wiki/" + df['item'].str.replace(" ", "_")
    df['color'] = None
    df['is_primary'] = df['item'].isin(primary_items)
    df = df.sort_values('item')
    df.to_csv(r"data/items.csv", index=False)
    # print(df)
