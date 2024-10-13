# main.py (modularized version)
import yaml
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from rpi_ws281x import Adafruit_NeoPixel, ws
from animations import run_rainbow_animation, run_blink_animation, clear_strip
from menu import options_menu
from utils import setup_logging, load_config, map_strip_type

# Set up logging
logger = setup_logging("SK6812Main")

@dataclass
class LEDConfig:
    count: int
    pin: int
    freq_hz: int = 800000
    dma: int = 10
    invert: bool = False
    brightness: int = 255
    channel: int = 0
    strip_type: str = "WS2811_STRIP_GRB"

# Load configuration from YAML file
config_data = load_config("config.yaml")

# Map string strip type to corresponding constant value
config_data["strip_type"] = map_strip_type(config_data["strip_type"], ws.WS2811_STRIP_GRB)
config = LEDConfig(**config_data)

# Create NeoPixel object with appropriate configuration
strip = Adafruit_NeoPixel(
    config.count, config.pin, config.freq_hz, config.dma, config.invert, config.brightness, config.channel, config.strip_type
)
strip.begin()

stop_event = threading.Event()
executor = ThreadPoolExecutor(max_workers=1)

# Dictionary for dynamic animation mapping
animations = {
    "1": run_rainbow_animation,
    "2": run_blink_animation,
    # Weitere Animationen können hier hinzugefügt werden
}

def display_menu():
    print("Select an option:")
    print("1: Rainbow Animation")
    print("2: Blink Animation")
    print("3: Options")
    print("0: Exit")

def handle_user_choice(choice, animation_future):
    # Stop any running animation before starting a new one
    if choice in animations:
        stop_event.set()
        if animation_future is not None:
            animation_future.result()  # Wait for the current animation to stop

        # Clear the stop event and run the selected animation
        stop_event.clear()
        return executor.submit(animations[choice], strip, stop_event)
    elif choice == "3":
        options_menu(strip)
    elif choice == "0":
        logger.info("Exiting program")
        return None
    else:
        print("Invalid choice. Please enter a valid option.")
    return animation_future

def main():
    logger.info("Starting LED animation selection menu")

    animation_future = None

    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ")
            animation_future = handle_user_choice(choice, animation_future)
            if choice == "0":
                break
    except KeyboardInterrupt:
        logger.info("Program interrupted by user in menu")
    finally:
        # Ensure any running animation is stopped
        stop_event.set()
        if animation_future is not None:
            animation_future.result()
        clear_strip(strip)
        executor.shutdown(wait=True)  # Wartet, bis alle Threads beendet sind

if __name__ == "__main__":
    main()