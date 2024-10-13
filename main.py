# https://github.com/rpi-ws281x/rpi-ws281x-python
# sudo pip install rpi_ws281x
from rpi_ws281x import *
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SK6812")

# LED strip configuration
@dataclass
class LEDConfig:
    count: int = 144     # Number of LED pixels
    pin: int = 18        # GPIO pin connected to the pixels (18 uses PWM!)
    freq_hz: int = 800000  # LED signal frequency in hertz (usually 800khz)
    dma: int = 10        # DMA channel to use for generating signal (try 10)
    brightness: int = 255  # Set to 0 for darkest and 255 for brightest
    invert: bool = False # True to invert the signal (when using NPN transistor level shift)
    channel: int = 0     # set to '1' for GPIOs 13, 19, 41, 45 or 53
    strip_type: int = ws.SK6812_STRIP_GRBW  # Strip type and colour ordering

config = LEDConfig()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(config.count, config.pin, config.freq_hz, config.dma, config.invert, config.brightness, config.channel, config.strip_type)
# Intialize the library (must be called once before other functions).
strip.begin()

# Global flag to stop the current animation
stop_event = threading.Event()
executor = ThreadPoolExecutor(max_workers=1)

class RGBColor:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def to_color(self):
        return Color(self.r, self.g, self.b)

    @staticmethod
    def from_tuple(color_tuple):
        return RGBColor(color_tuple[0], color_tuple[1], color_tuple[2])

def run_rainbow_animation():
    logger.info("Running rainbow animation")
    run_colors = [
        RGBColor(5, 0, 0),
        RGBColor(0, 5, 0),
        RGBColor(0, 0, 5),
        RGBColor(5, 0, 0)
    ]

    l = strip.numPixels()
    lc = len(run_colors) - 1
    bl = l / lc

    logger.debug(f"Total number of pixels: {l}")
    logger.debug(f"Number of color blocks: {lc}")
    logger.debug(f"Block length: {bl}")

    try:
        for startPos in range(l):
            if stop_event.is_set():
                logger.info("Stopping rainbow animation")
                break

            logger.debug(f"Start position: {startPos}")
            for i in range(l):
                relPos = (i - startPos) % bl
                block = int((i - startPos) // bl % lc)
                factors = (relPos * 1.0 / bl, (bl - relPos) * 1.0 / bl)

                red = run_colors[block + 1].r * factors[0] + run_colors[block].r * factors[1]
                green = run_colors[block + 1].g * factors[0] + run_colors[block].g * factors[1]
                blue = run_colors[block + 1].b * factors[0] + run_colors[block].b * factors[1]

                color = Color(int(red), int(green), int(blue))
                strip.setPixelColor(i, color)

            strip.show()
            time.sleep(50 / 1000.0)
    except Exception as e:
        logger.error(f"Unexpected error in rainbow animation: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up and turning off LEDs after rainbow animation")
        clear_strip()

def run_blink_animation():
    logger.info("Running blink animation")
    l = strip.numPixels()
    try:
        while not stop_event.is_set():
            # Turn all LEDs on (white)
            set_all_pixels(Color(255, 255, 255))
            time.sleep(0.5)

            # Turn all LEDs off
            set_all_pixels(Color(0, 0, 0))
            time.sleep(0.5)
    except Exception as e:
        logger.error(f"Unexpected error in blink animation: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up and turning off LEDs after blink animation")
        clear_strip()

def options_menu():
    try:
        while True:
            print("Options Menu:")
            print("1: Set Brightness")
            print("0: Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == "1":
                try:
                    brightness = int(input("Enter brightness (0-255): "))
                    if 0 <= brightness <= 255:
                        strip.setBrightness(brightness)
                        strip.show()
                        logger.info(f"Brightness set to {brightness}")
                    else:
                        print("Invalid brightness value. Please enter a number between 0 and 255.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 255.")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    except KeyboardInterrupt:
        logger.info("Options menu interrupted by user")

def set_all_pixels(color):
    l = strip.numPixels()
    for i in range(l):
        strip.setPixelColor(i, color)
    strip.show()

def clear_strip():
    set_all_pixels(Color(0, 0, 0))

def main():
    logger.info("Starting LED animation selection menu")

    animation_future = None

    try:
        while True:
            print("Select an option:")
            print("1: Rainbow Animation")
            print("2: Blink Animation")
            print("3: Options")
            print("0: Exit")

            choice = input("Enter your choice: ")

            # Stop any running animation, except for options menu
            if choice in ["1", "2"]:
                stop_event.set()
                if animation_future is not None:
                    animation_future.cancel()

            if choice == "1":
                stop_event.clear()
                animation_future = executor.submit(run_rainbow_animation)
            elif choice == "2":
                stop_event.clear()
                animation_future = executor.submit(run_blink_animation)
            elif choice == "3":
                options_menu()
            elif choice == "0":
                logger.info("Exiting program")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    except KeyboardInterrupt:
        logger.info("Program interrupted by user in menu")
    finally:
        # Ensure any running animation is stopped
        stop_event.set()
        if animation_future is not None:
            animation_future.cancel()
        clear_strip()

if __name__ == "__main__":
    main()