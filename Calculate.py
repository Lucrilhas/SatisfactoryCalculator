import networkx as nx
from utils import *


def get_first_non_primary(leaves, primarys=primary_clean_items):
    for l in leaves:
        if l not in primarys:
            return l
    return False


def verify_stop(leaves, primarys=primary_clean_items, max_iteration=51):
    logger.debug("Folhas: \t\t" + str(leaves))
    logger.debug("Primarios: \t" + str([True if l in primarys else False for l in leaves ]))
    r = any(l not in primarys for l in leaves)
    if r:
        logger.info("Ainda existem folhas não primarias --> Continuando Loop!")
    else:
        logger.warning("NÃO existem folhas não primarias --> PARANDO Loop!")
        
    return r

cool_itens = ["Wire", "Rotor", "Reinforced Iron Plate", "Cable", "Motor", "Copper Sheet"]
def calculate_all_options(target_item=cool_itens[5], draw=False, max_iteration= 51):
    ppp = 0
    all_recipes = read_json("jsons/recipes.json")
    if target_item not in all_recipes.keys():
        logger.error("Item não reconhecido: " + str(target_item))
        exit()

    graph = nx.DiGraph()
    graph.add_node(target_item)

    while verify_stop(get_leaves(graph)):
        folha = get_first_non_primary(get_leaves(graph))

        logger.info("Processando folha: " + str(folha))

        for recipe_name, recipe_values in all_recipes.get(folha).get("recipes").items():
            if recipe_name not in blacklist_recipes and recipe_values.get('byproduct') == False:
                rc = "Recipe: " + recipe_name
                graph.add_node(rc)
                graph.add_edge(folha, rc)

                for ing in recipe_values.get("ingredients"):
                    graph.add_node(ing['item_name'])
                    graph.add_edge(rc, ing['item_name'])
                    
                for prod in recipe_values.get("products"):
                    graph.add_node(prod['item_name'])
                    graph.add_edge(prod['item_name'], rc)
                

        if ppp == max_iteration:
            logger.error("PARADA POR ITERAÇÕES!!")
            break
        ppp +=1

    if draw:
        colors, label_colors = get_colors(graph, all_recipes, do_label=True)
        desenha_grafo(graph, colors)
    return graph

