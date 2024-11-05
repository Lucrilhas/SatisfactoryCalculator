from utils import *
import networkx as nx

def create_graph(target_item="Reinforced Iron Plate"):
    full_data = read_json("jsons/recipes.json")
    if not target_item in full_data:
        raise ValueError("Item não existe")

    options = []
    