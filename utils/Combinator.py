from itertools import product
from utils import logger

def generate_combinations(input_list):
    if not isinstance(input_list, list):
        return []
    input_list = [il for il in input_list if il]

    try:
        # if len(input_list) == 1:
        #     return input_list
        return list(product(*input_list))
    except TypeError:
        logger.critical("TypeError: " + str(input_list))
        return []

# input_data = [
#     [('l', 0), ('l', 1), ('l', 2)],
#     [('m', 0)],
#     [('n', 0), ('n', 1)]
# ]

# print(generate_combinations(input_data))