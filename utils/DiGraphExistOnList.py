import networkx as nx

def recipes_used(graph):
    return set(n.replace("Recipe: ", "") for n in graph.nodes if "Recipe: " in n)


def digraph_exist_on_list(digraph_list, new_digraph):
    recipes_on_new = recipes_used(new_digraph)
    # print(recipes_on_new)
    for existing_digraph in digraph_list:
        if recipes_used(existing_digraph) == recipes_on_new:
            return True
    return False