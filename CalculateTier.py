from utils import *

def define_tiers():
    full_data = read_json("jsons/recipes.json")

    items_names = [item_name for item_name in full_data]

    while items_names:
        for
    for item_name in full_data:
        logger.debug(item_name)
        # ===== TIER 0
        if full_data.get(item_name).get('primary', False):
            logger.warning("TIER 0")
            continue
        
        # ===== TIER 1
        for recipe_name in full_data.get(item_name).get('recipes'):
            recipe = full_data.get(item_name).get('recipes').get(recipe_name)
            all_primary = True
            for ingredient in recipe.get('ingredients'):
                if full_data.get(ingredient.get('item_name')).get('primary', False) == False:
                    all_primary = False
                    break
            if all_primary:
                logger.warning("TIER 1 -- " + recipe_name)
        