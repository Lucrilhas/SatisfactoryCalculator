
from .GetLogger import logger


primary_itens = (
    "Nitrogen Gas",
    "Excited Photonic Matter",
    "Bauxite",
    "Caterium Ore",
    "Coal",
    "Copper Ore",
    "Iron Ore",
    "Limestone",
    "Raw Quartz",
    "Sulfur"
)

blacklist = (
    "Beacon",
    "Boom Box",
    "Xeno-Zapper",
    "Zipline",
    "Xeno-Basher",
    "Jetpack",
    "Hoverpack",
    "Blade Runners",
    "Factory Cart™",
    "Gas Mask",
    "Golden Factory Cart™",
    "Hazmat Suit",
    "Nobelisk Detonator",
    "Medicinal Inhaler",
    "Object Scanner",
    "Parachute",
    "Portable Miner",
    "Rebar Gun",
    "Rifle"
)

__all__ = [
    "logger",
    "primary_itens",
    "blacklist",
]