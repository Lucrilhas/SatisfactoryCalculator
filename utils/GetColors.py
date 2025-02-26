from networkx import DiGraph
from pandas import DataFrame

def get_colors(graph:DiGraph, items: DataFrame):
    color_dict = dict(zip(items["item"], items["color"]))
    colors = []
    for node in graph.nodes():
        color = color_dict.get(node, '#FFFFFF') # Default to white if not found
        if color == '#FFFFFF' and "By product: " in node:
            color = color_dict.get(node[12:], '#FFFFFF') 
        colors.append(color)
    return colors


def get_labels_colors(colors):
    label_colors = []
    for color in colors:
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        brightness = (r*299 + g*587 + b*114) / 1000
        label_colors.append('#FFFFFF' if brightness < 128 else '#000000')
    return label_colors