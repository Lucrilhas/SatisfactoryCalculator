

def get_colors(graph, recipes, do_label=False):
    colors = []
    for node in graph.nodes():
        if r := recipes.get(node):
            colors.append(r.get("hex_color"))
        else:
            colors.append('#FFFFFF')
    if not do_label:
        return colors

    label_colors = []

    for color in colors:
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        brightness = (r*299 + g*587 + b*114) / 1000
        label_colors.append('#FFFFFF' if brightness < 128 else '#000000')
    return colors, label_colors