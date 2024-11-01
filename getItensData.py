import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from utils import logger

def scrape_all_items_wiki(url: str) -> list[str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.debug(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return [i["href"] for i in soup.select("#mw-pages ul li a")]

    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None
    except Exception as e:  # Catch other potential exceptions during parsing
        logger.error(f"An error occurred during parsing: {e}")
        return None

def scrape_item_wiki(url:str) -> dict:
    logger.info(url)
    soup = BeautifulSoup(url, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable sortable recipetable'})

    if not tables:
        return None

    data_list = []
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 5:
                try:
                    item_data = {
                        'input': cols[1].text.strip(), #Ingredients
                        'output': cols[3].text.strip(), #Products
                        'machine': cols[2].text.strip().split('\n')[0], #Machine name (handles possible line breaks)
                        'time': cols[2].text.strip().split('\n')[-1].split(' ')[0], #Time (extract number)
                        'energy': 'N/A'
                    }
                    data_list.append(item_data)
                except (IndexError, ValueError) as e:
                    print(f"Error parsing row: {e}")

    print(data_list)
    return data_list


if __name__ == "__main__":
    load_dotenv()
    all_itens_url = os.getenv("ALL_ITENS_PAGE")
    logger.info(all_itens_url)
    items_links = scrape_all_items_wiki(all_itens_url)

    if items_links:
        # for i in items_links:
        #     print(i)
        scrape_item_wiki(items_links[2])