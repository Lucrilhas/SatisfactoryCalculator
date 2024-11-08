from PIL import Image
from utils import logger
import numpy as np


def get_main_color(image_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        img_array = np.array(img)

        non_transparent_rows, non_transparent_cols = np.where(img_array[:, :, 3] > 0)
        
        if len(non_transparent_rows) == 0:  # Entirely transparent image
            return None

        min_row = np.min(non_transparent_rows)
        max_row = np.max(non_transparent_rows)
        min_col = np.min(non_transparent_cols)
        max_col = np.max(non_transparent_cols)


        cropped_array = img_array[min_row:max_row+1, min_col:max_col+1]
        colors, counts = np.unique(cropped_array.reshape(-1, 4), axis=0, return_counts=True)

        # Filter out transparent colors
        non_transparent_colors = colors[colors[:, 3] > 0]
        non_transparent_counts = counts[colors[:, 3] > 0]
        
        if len(non_transparent_counts) == 0:
            return None

        most_frequent = tuple(non_transparent_colors[np.argmax(non_transparent_counts)][:3])
        hex_color = '#%02x%02x%02x' % most_frequent 
        return hex_color

    except FileNotFoundError:
        logger.error(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None