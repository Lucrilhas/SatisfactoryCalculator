import networkx as nx
from utils import *
import copy
import pandas as pd

def get_leaves(graph):
    leaves = [node for node in graph.nodes() if not list(nx.descendants(graph, node))]
    return leaves
    

def all_leaves_are_primary(graph, do_print=True):
    leaves = get_leaves(graph)
    aux = all([l in primary_items for l in leaves])
    if do_print:
        logger.debug(aux)
    return aux


def first_leave_non_primary(leaves):
    for l in leaves:
        if l not in primary_items:
            return l
    return False


def calculate_all_graph(target_item: str, items:pd.DataFrame, recipes:pd.DataFrame, max_iterations: int = 101):
    if target_item not in items['item'].values:
        logger.error("Item não reconhecido: " + str(target_item))
        recipes
        exit()

    graph = nx.DiGraph()
    graph.add_node(target_item)
    
    for iteration in range(max_iterations):
        leaf = first_leave_non_primary(get_leaves(graph))
        r = recipes[recipes['product'] == leaf].fillna(value=False)
        for index, row in r.iterrows():
            graph.add_node("Recipe: " + row['recipe'])
            
            graph.add_node(row['product'])
            graph.add_edge(row['product'], "Recipe: " + row['recipe'])

            if row['by_product']:
                logger.warning(row['by_product'])
                graph.add_node(row['by_product'])
                graph.add_edge(row['by_product'], "Recipe: " + row['recipe'])

            for i in range(4):
                id = f'ingredient {i}'
                if row[id]:
                    logger.warning(row[id])
                    graph.add_node(row[id])
                    graph.add_edge("Recipe: " + row['recipe'], row[id])
                    

        logger.info(iteration)
        logger.info(get_leaves(graph))
        logger.info(all_leaves_are_primary(graph))
        print()
        
        if all_leaves_are_primary(graph):
            return graph

    logger.error("PARADA POR ITERAÇÕES!!")
    