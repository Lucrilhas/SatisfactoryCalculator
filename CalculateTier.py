from utils import *

def define_tiers():
    full_data = read_json("jsons/recipes.json")

    data = []
    for item_name in full_data:
        for recipe_name in full_data.get(item_name).get('recipes', [None]):
            data.append([item_name, recipe_name])

    prev = len(data)
    while data:
        logger.info(prev)
        indices_to_remove = []
        for indc, (item_name, recipe_name) in enumerate(data):
            # logger.debug((item_name, recipe_name))
            
            # ===== TIER 0
            if recipe_name is None:
                logger.warning(f"TIER 0 --- {item_name} --- {recipe_name}")
                indices_to_remove.append(indc)
                full_data[item_name]['max_tier'] = 0
                continue

            # ===== TIER 1++
            ingredients = [ing.get('item_name') for ing in full_data.get(item_name).get('recipes').get(recipe_name).get('ingredients')]
            ingredients_tiers = []
            for ing in ingredients:
                # print(ing)
                if full_data.get(ing).get('primary') == True:
                    ingredients_tiers.append(0)
                else:
                    ing_tier = [full_data.get(ing).get('recipes').get(r).get('max_tier') for r in full_data.get(ing).get('recipes')]
                    # print(ing_tier)
                    if None in ing_tier:
                        ingredients_tiers.append(None)
                    else:
                        ingredients_tiers.append(max(ing_tier))

            if None in ingredients_tiers:
                continue

            full_data[item_name]['recipes'][recipe_name]['max_tier'] = max(ingredients_tiers) + 1
            logger.warning(f"TIER {max(ingredients_tiers) + 1} --- {item_name} --- {recipe_name}")
            indices_to_remove.append(indc)
        data = [item for i, item in enumerate(data) if i not in indices_to_remove]
        print(len(data))
        if len(data) == prev:
            break
        prev = len(data)
            # for recipe_name in full_data.get(item_name).get('recipes'):
            #     recipe = full_data.get(item_name).get('recipes').get(recipe_name)
            #     all_primary = True
            #     for ingredient in recipe.get('ingredients'):
            #         if full_data.get(ingredient.get('item_name')).get('primary', False) == False:
            #             all_primary = False
            #             break
            #     if all_primary:
            #         logger.warning(f"TIER 1 --- {item_name} --- {recipe_name}")
            #         items_names.pop(lenn - indc - 1)
            #         full_data[item_name]['max_tier'] = 1
            #         continue

            # for recipe_name in full_data.get(item_name).get('recipes'):
            #     recipe = full_data.get(item_name).get('recipes').get(recipe_name)
            #     tiers = [ingredient.get('max_tier') for ingredient in recipe.get('ingredients')]
            #     if None in tiers:
            #         continue
            #     full_data[item_name]['max_tier'] = max(tiers) + 1
                
            #     logger.warning(f"TIER {max(tiers) + 1} --- {item_name} --- {recipe_name}")