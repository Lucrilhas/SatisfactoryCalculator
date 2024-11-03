
from .GetLogger import logger
from .GetMainColor import get_main_color
from .ReadRecipes import read_recipes


primary_items = (
    "Bacon_Agaric",
    "Bauxite",
    "Beryl_Nut",
    "Caterium_Ore",
    "Coal",
    "Copper_Ore",
    "Crude_Oil",
    "Excited_Photonic_Matter",
    "Iron_Ore",
    "Leaves",
    "Limestone",
    "Mycelia",
    "Nitrogen_Gas",
    "Paleberry",
    "Raw_Quartz",
    "SAM",
    "Sulfur",
    "Water"
    "Wood",
)

blacklist = (
    "Beacon",
    "Blade_Runners",
    "Boom_Box",
    "Color_Cartridge",
    "Cup",
    "Factory_Cart™",
    "FICSIT_Coupon",
    "FICSMAS/Equipment",
    "Flower_Petals",
    "Gas_Mask",
    "Golden Factory_Cart™",
    "Hard_Drive",
    "Hazmat_Suit",
    "Hoverpack",
    "HUB_Parts",
    "Jetpack",
    "Medicinal_Inhaler",
    "Mercer_Sphere",
    "Nobelisk_Detonator",
    "Object_Scanner",
    "Parachute",
    "Portable_Miner",
    "Rebar_Gun",
    "Rifle",
    "Somersloop",
    "Statues",
    "User:Ondar111/sandbox",
    "Vines",
    "Xeno-Basher",
    "Xeno-Zapper",
    "Zipline"
)

__all__ = [
    "logger",
    "primary_items",
    "blacklist",
    "get_main_color",
    "read_recipes"
]