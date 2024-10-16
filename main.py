# main.py (modularized version)
import yaml
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from rpi_ws281x import *
from animations import *
from menu import options_menu, selected_audio_device
from utils import *

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
    "3": run_fade_animation,
    "4": run_color_wipe_animation,
    "5": run_theater_chase_animation,
    "6": run_pulse_animation,
    "7": run_twinkle_animation,
    "8": run_wave_animation,
    "9": run_firework_animation,
    "10": run_meteor_animation,
    "11": run_larson_scanner_animation,
    "12": run_comet_animation,
    "13": run_bouncing_balls_animation,
    "14": run_soft_white_pulse_animation,
    "15": run_warm_white_fade_animation,
    "16": run_rainbow_with_white_flash_animation,
    "17": run_cool_white_twinkle_animation,
    "18": run_white_comet_animation,
    "19": run_aurora_borealis_animation,
    "20": run_fireplace_animation,
    "21": run_comet_rain_animation,
    "22": run_lightning_storm_animation,
    "23": run_pixel_explosion_animation,
    "24": run_strobe_effect,
    "25": run_holiday_twinkle_animation,
    "26": run_lava_explosion_animation,
    "29": run_random_sparkles_animation,
    "30": run_random_meteor_shower_animation,
    "32": run_random_white_strobes_animation,
    "33": run_random_color_shifts_animation,
    "34": run_random_walk_animation,
    "35": run_random_glitter_animation,
    # music sync
    "50": run_music_synchronized_wave,
}

def display_menu():
    print("Select an animation:")
    for key in sorted(animations.keys()):
        print(f"{key}: {animations[key].__name__.replace('_', ' ').title()}")
    print("0: Exit")

def handle_user_choice(choice, animation_future):
    if choice in animations:
        stop_event.set()
        if animation_future is not None:
            animation_future.result()  # Wait for the current animation to stop

        stop_event.clear()
        if choice == "50":  # Musik-synchronisierte Animation
            if selected_audio_device is None:
                print("No audio device selected. Please choose an audio input device from the options menu.")
                return animation_future
            return executor.submit(animations[choice], strip, stop_event, selected_audio_device)
        else:
            return executor.submit(animations[choice], strip, stop_event)
    elif choice.lower() == "o":
        options_menu(strip)  # Optionen-Menü aufrufen
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
        logger.info("Program interrupted by user")
    finally:
        stop_event.set()
        if animation_future is not None:
            animation_future.result()
        clear_strip(strip)
        executor.shutdown(wait=True)

if __name__ == "__main__":
    main()