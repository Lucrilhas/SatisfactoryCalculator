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


def save_all_links():
    os.makedirs(r"data", exist_ok=True)
    load_dotenv()
    main_page_link = os.getenv("MAIN_PAGE")
    all_itens_url = main_page_link + os.getenv("ALL_ITENS_PAGE")
    all_fuilds_url = main_page_link + os.getenv("ALL_FLUIDS_PAGE")
    logger.info([all_itens_url, all_fuilds_url])
    all_items = scrape_wiki_all_items(all_itens_url) + scrape_wiki_all_items(all_fuilds_url)
    
    items = [item for item in all_items if item not in blacklist_items]
    df = pd.DataFrame(items, columns=['items'])
    df['link'] = main_page_link + "/wiki/" + df['items'].str.replace(" ", "_")
    df = df.sort_values('items')
    df['color'] = None
    df.to_csv(r"data/items.csv", index=False)
    print(df)

