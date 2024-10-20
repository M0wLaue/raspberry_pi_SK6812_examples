# settings.py

from dataclasses import dataclass
import yaml
from rpi_ws281x import Color, ws

@dataclass
class AnimationSettings:
    speed: int = 50
    meteor_size: int = 10
    decay: float = 0.8
    tail_length: int = 5
    num_balls: int = 3
    ball_colors: list = None
    comet_color: Color = Color(0, 0, 255)
    glitter_probability: float = 0.1
    explosion_probability: float = 0.05

    def to_kwargs(self):
        # Konvertiere alle Attribute der Klasse zu einem Wörterbuch, das als **kwargs genutzt werden kann
        return self.__dict__
    
@dataclass
class LEDConfig:
    count: int = 150  # Anzahl der LEDs im Streifen
    pin: int = 18  # GPIO-Pin
    freq_hz: int = 800000
    dma: int = 10
    invert: bool = False
    brightness: int = 255
    channel: int = 0
    strip_type: str = "WS2811_STRIP_GRB"

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

def load_config(config_path):
    """
    Load the configuration from a YAML file.
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

class SettingsManager:
    _instance = None

    @staticmethod
    def get_instance():
        if SettingsManager._instance is None:
            SettingsManager()
        return SettingsManager._instance

    def __init__(self, config_path="hardware-config.yaml"):
        if SettingsManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SettingsManager._instance = self

        # Initialisiere Einstellungen
        self.config_path = config_path
        self.led_config = None
        self.animation_settings = AnimationSettings()
        self.selected_audio_device = None

        # Lade die LED-Konfiguration
        self.load_led_config()

    def load_led_config(self):
        # Load configuration from YAML file
        config_data = self._load_yaml(self.config_path)

        # Map string strip type to corresponding constant value
        config_data["strip_type"] = map_strip_type(config_data["strip_type"], ws.WS2811_STRIP_GRB)
        self.led_config = LEDConfig(**config_data)

    @staticmethod
    def _load_yaml(path):
        with open(path, "r") as f:
            return yaml.safe_load(f)

