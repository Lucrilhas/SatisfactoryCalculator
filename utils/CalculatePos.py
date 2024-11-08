from utils import logger, primary_clean_items
import networkx as nx
import copy

def calculate_pos(graph: nx.DiGraph, target_item: str, primarys: list = primary_clean_items):
    tiers = []
    current_indc = 0
    fila = [target_item]
    proxs = []
    used = set()

    while fila:
        if len(tiers) <= current_indc:
            tiers.append([])

        for item in fila:
            # print(item)
            # print(list(graph.successors(item)))
            # print(list(graph.predecessors(item)))
            
            if item not in used:
                tiers[current_indc].append(item)
                used.add(item)
                for suc in graph.successors(item):
                    if suc not in used:
                        proxs.append(suc)
                for pred in graph.predecessors(item):
                    if pred not in used:
                        tiers[current_indc-1].append(pred)
                        used.add(pred)

        logger.debug("Fila: " + str(fila))
        logger.debug("Prox: " + str(proxs))
        fila = copy.deepcopy(proxs)
        proxs = []
        current_indc += 1

    prims = []
    for t_index, t in enumerate(tiers):
        for i in t:
            if i in primarys:
                prims.append(i)
                tiers[t_index].remove(i)
    tiers.append(prims)

    for i, t in enumerate(tiers):
        print(i)
        print(t)