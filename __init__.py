# from unused.CalculateTier import define_tiers
# from unused.CreateGraph import create_graph
from Calculate import calculate_all_options, calculate_options
from Scrap.ScrapData import get_links_data
from Scrap.ScrapLinks import save_all_links

# from unused.presetPlots import preset_mock, preset_mock_plotly_two
from utils import *
import networkx as nx

if __name__ == "__main__":
    # save_all_links()
    # get_links_data()
    # create_graph()

    recipes = read_json("jsons/recipes.json")
    # preset_mock_plotly_two(recipes)
    # preset_mock(recipes)
    # cool_itens = ["Wire", "Rotor", "Reinforced Iron Plate", "Cable", "Motor", "Copper Sheet"]
    # target_items = "Steel Ingot"
    # target_items = "Steel Pipe"
    target_items = "Fuel"
    options_graph = calculate_all_options(target_items, recipes)

    colors = get_colors(options_graph, recipes)
    desenha_grafo(options_graph, colors)
    # print("\n====================================\n")

    options = calculate_options(target_items, options_graph, recipes)
    for o in options:
        colors = get_colors(o, recipes)
        desenha_grafo(o, colors)
        

    # edges = [
    #     ("A", "Recipe: 0"),
    #     ("A", "Recipe: 1"),
    #     ("A", "Recipe: 3"),
    #     ("A", "Recipe: 4"),
    #     ("Recipe: 0", "B0"),
    #     ("Recipe: 0", "B1"),
    #     ("Recipe: 1", "B1"),
    #     ("Recipe: 1", "C0"),
    #     ("C0", "Recipe: 2"),
    #     ("Recipe: 2", "C1"),
    #     ("Recipe: 2", "C2"),
    #     ("Recipe: 3", "D0"),
    #     ("Recipe: 9", "D1"),
    #     ("D0", "Recipe: 9"),
    #     ("D2", "Recipe: 9"),
    #     ("E", "Recipe: 3"),
    #     ("Recipe: 4", "F0"),
    #     ("F0", "Recipe: 5"),
    #     ("F0", "Recipe: 6"),
    #     ("Recipe: 5", "F1"),
    #     ("Recipe: 6", "F2"),
    #     ("Recipe: 4", "G0"),
    #     ("G0", "Recipe: 7"),
    #     ("G0", "Recipe: 8"),
    #     ("Recipe: 7", "G1"),
    #     ("Recipe: 8", "G2"),
    # ]
    # edges = [
    #     ("A", "Recipe: 0"),
    #     ("A", "Recipe: 1"),
    #     ("Recipe: 0", "B"),
    #     ("Recipe: 1", "C"),
    #     ("B", "Recipe: 2"),
    #     ("B", "Recipe: 3"),
    #     ("C", "Recipe: 4"),
    #     ("C", "Recipe: 5"),
    #     ("Recipe: 2", "D"),
    #     ("Recipe: 3", "E"),
    #     ("Recipe: 4", "F"),
    #     ("Recipe: 5", "G"),
    #     ("A", "Recipe: 6"),
    #     ("Recipe: 6", "H"),
    #     ("H", "Recipe: 7"),
    #     ("Recipe: 7", "I"),
    # ]
    # graph = nx.DiGraph(edges)

    # desenha_grafo(graph, colors=None)
    # calculate_options("A", graph, recipes)
