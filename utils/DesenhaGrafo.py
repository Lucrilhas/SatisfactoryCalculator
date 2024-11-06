import networkx as nx
import matplotlib.pyplot as plt

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