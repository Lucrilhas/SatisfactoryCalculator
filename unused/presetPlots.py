from utils import *
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def preset_mock(recipes: dict):
    g = {
        ("Reinforced Iron Plate", "Iron Plate"): 10,
        ("Reinforced Iron Plate", "Screw"): 5,
        ("Screw", "Iron Rod"): 7,
        ("Iron Rod", "Iron Ingot"): 3,
        ("Iron Ingot", "Iron Ore"): 9,
        ("Iron Plate", "Iron Ingot"): 1,
        ("Iron Plate", "Steel Ingot"): 7,
        ("Steel Ingot", "Iron Ingot"): 2,
        ("Steel Ingot", "Coal"): 7,
    }
    graph = nx.DiGraph()
    for (e1, e2), weight in g.items():
        graph.add_edge(e1, e2, weight=weight)

    leaves = get_leaves(graph)
    logger.critical(leaves)
    # nodes = list(set([item for sublist in g.keys() for item in sublist]))
    # logger.debug(nodes)
    colors_to_use = [recipes.get(node).get("hex_color") for node in graph.nodes()]
    # logger.warning(colors_to_use)

    fig, ax = plt.subplots(figsize=(12, 8))
    # ax.set_facecolor("lightblue")
    # pos = nx.spring_layout(graph)
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    nx.draw(
        graph,
        pos,
        ax=ax,
        with_labels=True,
        node_size=2000,
        font_color="#000000",
        font_weight="bold",
        node_color=colors_to_use,
        arrowsize=20,
        width=1,
    )
    fig.set_facecolor("lightblue")
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1.0, top=1.0, wspace=0.2, hspace=0.2)
    plt.show()


def preset_mock_plotly(recipes: dict):
    g = {
        ("Reinforced Iron Plate", "Iron Plate"): 10,
        ("Reinforced Iron Plate", "Screw"): 5,
        ("Screw", "Iron Rod"): 7,
        ("Iron Rod", "Iron Ingot"): 3,
        ("Iron Ingot", "Iron Ore"): 9,
        ("Iron Plate", "Iron Ingot"): 1,
        ("Iron Plate", "Steel Ingot"): 7,
        ("Steel Ingot", "Iron Ingot"): 2,
        ("Steel Ingot", "Coal"): 7,
    }
    graph = nx.DiGraph()
    for (e1, e2), weight in g.items():
        graph.add_edge(e1, e2, weight=weight)

    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")

    # Extract node and edge information for Plotly
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    for node, coordinates in pos.items():
        node_x.append(coordinates[0])
        node_y.append(coordinates[1])
        node_text.append(node)
        node_color.append(recipes.get(node, {}).get("hex_color", "#cccccc"))

    edge_x = []
    edge_y = []
    edge_text = []

    for source, target, weight in graph.edges(data=True):
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(str(weight['weight']))


    # Create Plotly figure
    fig = go.Figure(layout=go.Layout(
        plot_bgcolor='lightblue', # Set background color
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))

    # Add edges as scatter traces
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='black'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    ))



    # Add nodes as scatter traces
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='middle center',
        marker=dict(
            size=30,  # Adjust node size as needed
            color=node_color,  # Set node color
            line=dict(width=0) # Remove node outline
        ),
        hoverinfo='text'
    ))


    fig.show()



def preset_mock_plotly_two(recipes: dict):
    # G = nx.random_geometric_graph(200, 0.125)
    data = {
        ("Reinforced Iron Plate", "Iron Plate"): 10,
        ("Reinforced Iron Plate", "Screw"): 5,
        ("Screw", "Iron Rod"): 7,
        ("Iron Rod", "Iron Ingot"): 3,
        ("Iron Ingot", "Iron Ore"): 9,
        ("Iron Plate", "Iron Ingot"): 1,
        ("Iron Plate", "Steel Ingot"): 7,
        ("Steel Ingot", "Iron Ingot"): 2,
        ("Steel Ingot", "Coal"): 7,
    }
    G = nx.DiGraph()
    for (e1, e2), weight in data.items():
        G.add_edge(e1, e2, weight=weight)

    pos = nx.spring_layout(G)  # Or use other layouts like: nx.circular_layout, nx.kamada_kawai_layout, etc.

    for node, (x, y) in pos.items():
        G.nodes[node]['pos'] = (x, y)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title=dict(
                text='Node Connections',
                side='right'
                ),
                xanchor='left',
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title=dict(
                        text="<br>Network graph made with Python",
                        font=dict(
                            size=16
                        )
                    ),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code: <a href='https://plotly.com/python/network-graphs/'> https://plotly.com/python/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()
    
# if __name__ == "__main__":
#     recipes = read_recipes()
#     # while True:
#     #     item_objective = input("Escreva um item para produzir:\n")
#     #     if item_objective in recipes.keys():
#     #         break

#     # item_objective_pmin = float(input("Escreva Quantos itens por minuto:\n"))

#     # print(item_objective, item_objective_pmin)
#     # preset_mock(recipes)
#     # preset_mock_plotly(recipes)
#     preset_mock_plotly_two(recipes)


    # pos_methods = [
    #     "fdp",      # Gostei muito n
    #     "dot",      # Mais ou Menos
    #     "neato",    # Mais ou Menos
    #     "twopi",    # Mais ou Menos
    #     "sfdp",     # Meio Ok

    #     "circo",    # Circulo Merda
    #     "patchwork",    # Quadrado meio paia
    #     "osage",    # Quadrado tbm meio paia
    #     # N Funciona:
    #     "gc",
    #     "nop",
    #     "acyclic",
    #     "tred",
    #     "gvpr",
    #     "sccmap",
    #     "gvcolor",
    #     "unflatten",
    #     "ccomps",
    # ]