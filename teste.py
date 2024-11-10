def add_neighboors_based_on_other(aux, info_graph, son):

    for pred in paths_graph.predecessors(son):
        aux.add_node(pred)
        aux.add_edge(pred, son)

    for suc in paths_graph.successors(son):
        aux.add_node(suc)
        aux.add_edge(son, suc)