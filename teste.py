import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()
G.add_node("A very long\nnode name")
G.add_node("B")
G.add_edge("A very long\nnode name", "B")

# Choose a layout (adjust as needed)
pos = nx.spring_layout(G)

# Draw the graph with adjusted node label properties
node_labels = {node: node for node in G.nodes()}  #Simple labels, using node names directly.

nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=1500,
        node_color="lightblue", font_size=10, font_family="sans-serif") #font_size can be adjusted

# Improve label appearance - this is crucial for line breaks to work nicely
# Adjust the following values to fine-tune appearance
plt.tight_layout() # Helps prevent labels from being cut off.
plt.subplots_adjust(top=0.9) # Adds some extra space at the top


plt.show()