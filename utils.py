# utils.py
import yaml
import logging
from rpi_ws281x import ws

def setup_logging(name):
    """
    Set up logging with the given logger name.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(name)

def load_config(config_path):
    """
    Load the configuration from a YAML file.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def map_strip_type(strip_type_str, default):
    """
    Map a strip type string to the corresponding constant value from the ws library.
    """
    strip_type_mapping = {
        "WS2811_STRIP_RGB": ws.WS2811_STRIP_RGB,
        "WS2811_STRIP_RBG": ws.WS2811_STRIP_RBG,
        "WS2811_STRIP_GRB": ws.WS2811_STRIP_GRB,
        "WS2811_STRIP_GBR": ws.WS2811_STRIP_GBR,
        "WS2811_STRIP_BRG": ws.WS2811_STRIP_BRG,
        "WS2811_STRIP_BGR": ws.WS2811_STRIP_BGR,
        "SK6812_STRIP_RGBW": ws.SK6812_STRIP_RGBW,
        "SK6812_STRIP_GRBW": ws.SK6812_STRIP_GRBW
    }
    return strip_type_mapping.get(strip_type_str, default)