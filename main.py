# main.py (modularized version)
import yaml
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from rpi_ws281x import *
from animations import *
from menu import options_menu
from utils import *
from settings import SettingsManager
import pyaudio

# Set up logging
logger = setup_logging("SK6812Main")

# Lade die zentrale Einstellungsinstanz
settings = SettingsManager.get_instance()

# Erstelle NeoPixel Objekt mit den geladenen LED-Einstellungen
led_config = settings.led_config
strip = Adafruit_NeoPixel(
    led_config.count, led_config.pin, led_config.freq_hz, led_config.dma, led_config.invert, led_config.brightness, led_config.channel, led_config.strip_type
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
    "51": run_frequency_bands_gradient,
    "52": run_beat_pulse_animation,
    "53": run_wave_ripple_effect,
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
        animation_function = animations[choice]
        animation_args = [strip, stop_event]
        animation_kwargs = {}

        # Wenn die Musik-synchronisierte Animation gewählt wurde, stelle sicher, dass ein Audio-Eingabegerät ausgewählt ist
        if int(choice) >= 50:  # Musik-synchronisierte Animation
            if settings.selected_audio_device is None:
                p = pyaudio.PyAudio()
                if p.get_device_count() == 0:
                    print("No audio devices available.")
                    return animation_future
                else:    
                    settings.selected_audio_device = p.get_device_info_by_index(0)
                    print("Default device selected. Choose another audio input device from the options menu.")
                
            animation_args.append(settings.selected_audio_device)

        # Verwende die allgemeinen Animationseinstellungen für alle Animationen
        animation_kwargs = settings.animation_settings.to_kwargs()

        return executor.submit(animation_function, *animation_args, **animation_kwargs)
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