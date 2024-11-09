# from Calculate import calculate_all_options, calculate_options
from GraphProcessing import calculate_all_graph
from Scrap.ScrapData import get_recipes_data
from Scrap.ScrapImages import get_images_and_colors
from Scrap.ScrapLinks import get_items_links

from utils import *
import pandas as pd
# from utils.CalculatePos import calculate_pos
# import networkx as nx

if __name__ == "__main__":
    # get_items_links()
    # get_images_and_colors()
    # get_recipes_data()

    items = pd.read_csv("data/items.csv")
    recipes = pd.read_csv("data/recipes.csv")
    # print(recipes)

    # target_item = ["Wire", "Rotor", "Reinforced Iron Plate", "Cable", "Motor", "Copper Sheet"]
    # target_item = "Steel Ingot"
    # target_item = "Steel Pipe"
    target_item = "Fuel"
    # target_item = "Turbofuel"
    # target_item = "Rocket Fuel"
    # target_item = "Ionized Fuel"
    # target_item = "Thermal Propulsion Rocket"
    
    # options_graph = calculate_all_options(target_item, recipes)
    complete_graph = calculate_all_graph(target_item, items, recipes)

    # colors = get_colors(options_graph, recipes)
    # calculate_pos(options_graph, target_item, )
    desenha_grafo(complete_graph, None)
    # print("\n====================================\n")

    # options = calculate_options(target_item, options_graph, recipes)
    # logger.info(len(options))
    # for o in options:
    #     colors = get_colors(o, recipes)
    #     desenha_grafo(o, colors)
