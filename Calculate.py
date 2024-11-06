import networkx as nx
from utils import *
import matplotlib.pyplot as plt

def get_first_non_primary(leaves, primarys=primary_clean_items):
    for l in leaves:
        if l not in primarys:
            return l
    return False


def verify_stop(leaves, primarys=primary_clean_items):
    logger.debug("Folhas: \t\t" + str(leaves))
    logger.debug("Primarios: \t" + str([True if l in primarys else False for l in leaves ]))
    r = any(l not in primarys for l in leaves)
    if r:
        logger.info("Ainda existem folhas não primarias --> Continuando Loop!")
    else:
        logger.warning("NÃO existem folhas não primarias --> PARANDO Loop!")
        
    return r


def calculate(target_item="Iron Rod"):
    ppp = 0
    all_recipes = read_json("jsons/recipes.json")
    if target_item not in all_recipes.keys():
        logger.error("Item não reconhecido: " + str(target_item))
        exit()

    graph = nx.DiGraph()
    graph.add_node(target_item)
    # print(graph)
    # print(get_leaves(graph))

    #already_processed = set()

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
                

        if ppp == 51:
            logger.error("PARADA POR ITERAÇÕES!!")
            break
        ppp +=1

    colors, label_colors = get_colors(graph, all_recipes, do_label=True)
    desenha_grafo(graph, colors)


    


def desenha_grafo(graph, colors):
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    nx.draw(
        graph,
        pos,
        ax=ax,
        with_labels=True,
        bbox=dict(facecolor="red", alpha=.5),
        node_size=1000,
        font_color="#000000", # label_colors,
        font_weight="bold",
        font_size=12,
        node_color=colors,
        node_shape='s',
        arrowsize=20,
        width=0.5,
    )
    fig.set_facecolor("lightblue")
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.2, hspace=0.2)
    plt.show()