import os
import requests
from bs4 import BeautifulSoup
from utils import *
import pandas as pd


def scrape_image(name:str, item_link:str) -> str:
    # logger.debug(main_page_link + item_link)
    response = requests.get(item_link)
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


def get_images_and_colors():
    df = pd.read_csv(r"data/items.csv")
    images_filepaths = []
    for row in df.itertuples():
        logger.debug(f"{row.item}  ---  {row.link}")
        images_filepaths.append(scrape_image(row.item, row.link))
        
    logger.debug("Calculaing Colors...")
    df['color'] = df['item'].apply(lambda x: get_main_color(f"imgs/{x}.png"))
    logger.debug("Finished!")
    df.to_csv(r"data/items.csv", index=False)