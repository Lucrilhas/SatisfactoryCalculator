import json
from utils import logger

def read_recipes(filepath: str = r"data/recipes.json") -> dict:
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logger.error(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON format in {filepath}: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return None