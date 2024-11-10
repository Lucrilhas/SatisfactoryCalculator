import networkx as nx
from utils import *
import copy
import pandas as pd

def get_leaves(graph):
    leaves = [node for node in graph.nodes() if not list(nx.descendants(graph, node))]
    return leaves
    

def all_leaves_are_primary(graph, do_print=False):
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
        exit()
    pd.set_option('future.no_silent_downcasting', True)

    graph = nx.DiGraph()
    graph.add_node(target_item)
    
    for iteration in range(max_iterations):
        leaf = first_leave_non_primary(get_leaves(graph))
        r = recipes[recipes['product'] == leaf].fillna(value=False)
        r = r.infer_objects(copy=False)
        for index, row in r.iterrows():
            # recipe_name = "Recipe: " + row['recipe']
            recipe_name = f"Recipe: {row['recipe']}"
            graph.add_node(recipe_name)
            
            graph.add_node(row['product'])
            graph.add_edge(row['product'], recipe_name)

            if row['by_product']:
                graph.add_node("By product: " + row['by_product'])
                graph.add_edge("By product: " + row['by_product'], recipe_name)

            for i in range(4):
                id = f'ingredient {i}'
                if row[id]:
                    graph.add_node(row[id])
                    graph.add_edge(recipe_name, row[id])
                    

        # logger.info(iteration)
        # logger.info(get_leaves(graph))
        # logger.info(all_leaves_are_primary(graph))
        # print()
        
        if all_leaves_are_primary(graph):
            return graph

    logger.error("PARADA POR ITERAÇÕES!!")


def calculate_each_path(target_item: str, paths_graph:nx.DiGraph, max_iterations: int = 101):
    opcoes = [nx.DiGraph()]
    opcoes[0].add_node(target_item)
    paths = []

    for _ in range(max_iterations):
        if len(opcoes) == 0:
            logger.info("SAIR")
            return paths

        
        g = opcoes.pop(0)
        leaves = get_leaves(g)

        # Finalizar:
        if all_leaves_are_primary(g):
            # logger.info("Entrou aqui")
            # desenha_grafo(g, colors=None)
            paths.append(g)
            continue

        # Recipes:
        sucessors = []
        for l in leaves:
            sucessors.append([(l, suc) for suc in paths_graph.successors(l)])

        # print("Sucessors: " + str(sucessors))
        combinations = generate_combinations(sucessors)
        # print("Combinations: " + str(combinations))
        for comb in combinations:
            aux = copy.deepcopy(g)
            for parent, son in comb:
                for pred in paths_graph.predecessors(son):
                    aux.add_node(pred)
                    aux.add_edge(pred, son)

                for suc in paths_graph.successors(son):
                    aux.add_node(suc)
                    aux.add_edge(son, suc)
                if not digraph_exist_on_list(opcoes, aux):
                    opcoes.append(aux)
                    # opcoes_recipes.append(recipes_used)

        
        # print(combinations)

       #  break


    logger.error("PARADA POR ITERAÇÕES!!")