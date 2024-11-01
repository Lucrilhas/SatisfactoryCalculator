# def scrape_wiki_item_tables(url:str) -> dict:
#     logger.info(url)
#     response = requests.get(url)
#     response.raise_for_status()
#     # logger.debug(response)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     recipe_tables = soup.find_all('table', class_='wikitable sortable recipetable')

#     recipe_data = []

#     for table in recipe_tables:
#         for row in table.find_all('tr')[1:]:  # Skip header row
#             cells = row.find_all('td')
#             if len(cells) >= 5: #Ensure all expected cells are present

#                 name = cells[0].get_text(strip=True)

#                 ingredients = []
#                 for item in cells[1].find_all('div', class_='recipe-item'):
#                     amount = item.find('span', class_='item-amount').get_text(strip=True).replace('×','')
#                     ingredient_name = item.find('span', class_='item-name').get_text(strip=True)
#                     try:
#                         ingredients.append((ingredient_name, int(amount)))
#                     except ValueError: #Handle cases like "X ml" where amount is not a simple integer
#                         ingredients.append((ingredient_name, amount))

#                 produced_in = cells[2].get_text(strip=True).replace('\n',', ')

#                 products = []
#                 for item in cells[3].find_all('div', class_='recipe-item'):
#                    amount = item.find('span', class_='item-amount').get_text(strip=True).replace('×','')
#                    product_name = item.find('span', class_='item-name').get_text(strip=True)
#                    try:
#                       products.append((product_name, int(amount)))
#                    except ValueError:
#                        products.append((product_name,amount))
                
#                 unlocked_by = cells[4].get_text(strip=True).replace('\n', ', ')


#                 recipe_data.append({
#                     "name": name,
#                     "ingredients": ingredients,
#                     "produced_in": produced_in,
#                     "products": products,
#                     "unlocked_by": unlocked_by
#                 })

#     return recipe_data