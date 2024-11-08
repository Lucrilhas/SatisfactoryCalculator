import networkx as nx
from utils import *
import copy


def get_first_non_primary(leaves, primarys):
    for l in leaves:
        if l not in primarys:
            return l
    return False


def any_leaf_non_primary(leaves, primarys, do_print=True):
    logger.debug("Folhas: \t\t" + str(leaves))
    logger.debug("Primarios: \t" + str([True if l in primarys else False for l in leaves ]))
    r = any(l not in primarys for l in leaves)
    if do_print:
        if r:
            logger.info("Ainda existem folhas não primarias --> Continuando Loop!")
        else:
            logger.warning("NÃO existem folhas não primarias --> PARANDO Loop!")
        
    return r

def calculate_all_options(target_item, all_recipes, primarys=primary_clean_items, max_iteration=101):
    ppp = 0
    if target_item not in all_recipes.keys():
        logger.error("Item não reconhecido: " + str(target_item))
        exit()

    graph = nx.DiGraph()
    graph.add_node(target_item)

    while any_leaf_non_primary(get_leaves(graph), primarys):
        folha = get_first_non_primary(get_leaves(graph), primarys)

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

    return graph


def add_neighboors_based_on_other(main_graph, info_graph, node):
    # preds = list(info_graph.predecessors(node))
    # succs = list(info_graph.successors(node))
    for pred in info_graph.predecessors(node):
        main_graph.add_node(pred)
        main_graph.add_edge(pred, node)

    for suc in info_graph.successors(node):
        main_graph.add_node(suc)
        main_graph.add_edge(node, suc)

        # for suc_of_suc in info_graph.successors(node):
        #     main_graph.add_node(suc_of_suc)
        #     main_graph.add_edge(suc, suc_of_suc)


def calculate_options(target_item, info_graph, recipes, primarys=primary_clean_items, max_iteration=40):
    ppp=0
    opcoes = [nx.DiGraph()]
    opcoes[0].add_node(target_item)
    # opcoes_recipes = [{}]
    finais = []

    while opcoes:
        g = opcoes.pop(0)
        # opcoes_recipes.pop(0)
        leaves = get_leaves(g)

        # Finalizar:
        if not any_leaf_non_primary(leaves, primarys, do_print=False): # All Primary
            # logger.info("Entrou aqui")
            # desenha_grafo(g, colors=None)
            finais.append(g)
            continue

        # Recipes:
        sucessors = []
        for l in leaves:
            sucessors.append([(l, suc) for suc in info_graph.successors(l)])

        # print("Sucessors: " + str(sucessors))
        combinations = generate_combinations(sucessors)
        # print("Combinations: " + str(combinations))
        for comb in combinations:
            aux = copy.deepcopy(g)
            for parent, son in comb:
                add_neighboors_based_on_other(aux, info_graph, son)
                if not digraph_exist_on_list(opcoes, aux):
                    opcoes.append(aux)
                    # opcoes_recipes.append(recipes_used)
        # print(combinations)

        if ppp == max_iteration:
            logger.error("PARADA POR ITERAÇÕES!!")
            break
        ppp +=1
       #  break

    return finais
    logger.warning(len(finais))
    desenha_grafo(finais, colors=None)
        
        
    # Iniciar
    # for suc in options_graph.successors(target_item):
        
    #     g.add_node(suc)
    #     g.add_edge(target_item, suc)
    #     for suc_of_suc in options_graph.successors(suc):
    #         g.add_node(suc)
    #         g.add_node(suc_of_suc)
    #         g.add_edge(suc, suc_of_suc)
            
    #     ops.append(g)

    # ppp = 0
    # while ops:
    #     print(len(ops))
    #     g = ops[0]
    #     leaves = get_leaves(g)
    #     print(leaves)
    #     if not any_leaf_non_primary(leaves, primarys, do_print=False): # All Primary
    #         print("Entrou aqui")
    #         desenha_grafo(g, colors=None)
    #         fins.append(g)
    #         ops.pop(0)
    #         continue

    #     # combinations = []
    #     for l in leaves:
    #         if l not in primarys:
    #             logger.warning(l)
    #             preds = list(options_graph.predecessors(l))
    #             logger.warning(preds)
    #             if len(preds) > 0:
    #                 for pred in preds:
    #                     g.add_node(pred)
    #                     g.add_edge(pred, l)
                        
    #             succs = list(options_graph.successors(l))
    #             logger.warning(succs)
    #             if len(succs) == 1:
    #                 suc = succs[0]
    #                 g.add_node(suc)
    #                 g.add_edge(l, suc)
    #                 for suc_of_suc in options_graph.successors(suc):
    #                     g.add_node(suc_of_suc)
    #                     g.add_edge(suc, suc_of_suc)
                
    #             else:
    #                 pass
                    
                    
    #             # combinations.append(len(list(options_graph.successors(l))))

    #     # print(combinations)
            
            

    #     if ppp == max_iteration:
    #         logger.error("PARADA POR ITERAÇÕES!!")
    #         break
    #     ppp +=1

    # for g in fins:
    #     desenha_grafo(g, colors=None)
    # desenha_grafo(fins, colors=None)