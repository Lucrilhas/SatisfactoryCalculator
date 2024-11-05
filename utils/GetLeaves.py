from networkx import descendants

def get_leaves(graph):
    leaves = [node for node in graph.nodes() if not list(descendants(graph, node))]
    return leaves