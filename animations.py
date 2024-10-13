# animations.py
import time
import logging
from rpi_ws281x import Color
from threading import Event

logger = logging.getLogger("SK6812Animations")

def run_rainbow_animation(strip, stop_event: Event):
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

    try:
        for startPos in range(l):
            if stop_event.is_set():
                logger.info("Stopping rainbow animation")
                break

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
        clear_strip(strip)

def run_blink_animation(strip, stop_event: Event):
    logger.info("Running blink animation")
    l = strip.numPixels()
    try:
        while not stop_event.is_set():
            set_all_pixels(strip, Color(255, 255, 255))
            time.sleep(0.5)
            set_all_pixels(strip, Color(0, 0, 0))
            time.sleep(0.5)
    except Exception as e:
        logger.error(f"Unexpected error in blink animation: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up and turning off LEDs after blink animation")
        clear_strip(strip)

def set_all_pixels(strip, color):
    l = strip.numPixels()
    for i in range(l):
        strip.setPixelColor(i, color)
    strip.show()

def clear_strip(strip):
    set_all_pixels(strip, Color(0, 0, 0))

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
