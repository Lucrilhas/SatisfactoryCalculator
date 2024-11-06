# from unused.CalculateTier import define_tiers
# from unused.CreateGraph import create_graph
from Calculate import calculate
from Scrap.ScrapData import get_links_data
from Scrap.ScrapLinks import save_all_links
# from unused.presetPlots import preset_mock, preset_mock_plotly_two
from utils.ReadJson import read_json


if __name__ == "__main__":
    # save_all_links()
    # get_links_data()
    # create_graph()
    


    # recipes = read_json("jsons/recipes.json")
    # preset_mock_plotly_two(recipes)
    # preset_mock(recipes)
    calculate()
    pass
