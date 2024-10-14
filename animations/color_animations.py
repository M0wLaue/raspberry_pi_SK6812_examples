import time
import logging
import math
import random
from .animation_utils import run_generic_animation, set_all_pixels, set_all_pixels_rgbw, clear_strip, wheel_rgbw
from rpi_ws281x import Color
from threading import Event

logger = logging.getLogger("SK6812Animations")


def run_rainbow_animation(strip, stop_event: Event):
    logger.info("Running rainbow animation")
    run_colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 0, 0)
    ]
    l = strip.numPixels()
    lc = len(run_colors) - 1
    bl = l / lc

    def update_function(strip):
        for startPos in range(l):
            if stop_event.is_set():
                return
            for i in range(l):
                relPos = (i - startPos) % bl
                block = int((i - startPos) // bl % lc)
                factors = (relPos * 1.0 / bl, (bl - relPos) * 1.0 / bl)

                red = run_colors[block + 1][0] * factors[0] + run_colors[block][0] * factors[1]
                green = run_colors[block + 1][1] * factors[0] + run_colors[block][1] * factors[1]
                blue = run_colors[block + 1][2] * factors[0] + run_colors[block][2] * factors[1]

                color = Color(int(red), int(green), int(blue))
                strip.setPixelColor(i, color)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_blink_animation(strip, stop_event: Event):
    logger.info("Running blink animation")

    def update_function(strip):
        set_all_pixels(strip, Color(255, 255, 255))
        time.sleep(0.5)
        set_all_pixels(strip, Color(0, 0, 0))
        time.sleep(0.5)

    run_generic_animation(strip, stop_event, update_function, update_speed=500)


def run_color_wipe_animation(strip, stop_event: Event, color=Color(255, 0, 0)):
    logger.info("Running color wipe animation")
    l = strip.numPixels()

    def update_function(strip):
        for i in range(l):
            if stop_event.is_set():
                return
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(0.05)
        for i in range(l):
            if stop_event.is_set():
                return
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_pulse_animation(strip, stop_event: Event, color=Color(255, 0, 0), wait_ms=50):
    logger.info("Running pulse animation")

    def update_function(strip):
        for brightness in range(0, 256, 5):
            if stop_event.is_set():
                return
            set_all_pixels(strip, Color(color.r * brightness // 255, color.g * brightness // 255, color.b * brightness // 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
        for brightness in range(255, -1, -5):
            if stop_event.is_set():
                return
            set_all_pixels(strip, Color(color.r * brightness // 255, color.g * brightness // 255, color.b * brightness // 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)

    run_generic_animation(strip, stop_event, update_function, update_speed=wait_ms)


def run_soft_white_pulse_animation(strip, stop_event: Event, red=255, green=0, blue=0, max_white=255, speed=50):
    logger.info("Running soft white pulse animation")

    def update_function(strip):
        for white in range(0, max_white + 1, 5):
            if stop_event.is_set():
                return
            set_all_pixels_rgbw(strip, red, green, blue, white)
            strip.show()
            time.sleep(speed / 1000.0)
        for white in range(max_white, -1, -5):
            if stop_event.is_set():
                return
            set_all_pixels_rgbw(strip, red, green, blue, white)
            strip.show()
            time.sleep(speed / 1000.0)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_warm_white_fade_animation(strip, stop_event: Event, speed=100):
    logger.info("Running warm white fade animation")
    colors = [
        (255, 0, 0),  # Rot
        (0, 255, 0),  # Grün
        (0, 0, 255),  # Blau
        (255, 255, 0)  # Gelb
    ]

    def update_function(strip):
        for color in colors:
            for white in range(0, 256, 5):
                if stop_event.is_set():
                    return
                set_all_pixels_rgbw(strip, color[0], color[1], color[2], white)
                strip.show()
                time.sleep(speed / 1000.0)
            for white in range(255, -1, -5):
                if stop_event.is_set():
                    return
                set_all_pixels_rgbw(strip, color[0], color[1], color[2], white)
                strip.show()
                time.sleep(speed / 1000.0)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_rainbow_with_white_flash_animation(strip, stop_event: Event, flash_duration=0.2, rainbow_speed=50):
    logger.info("Running rainbow with white flash animation")

    def update_function(strip):
        for j in range(256):
            if stop_event.is_set():
                return
            for i in range(strip.numPixels()):
                color = wheel_rgbw((i + j) & 255)
                strip.setPixelColorRGB(i, color[0], color[1], color[2], 0)
            strip.show()
            time.sleep(rainbow_speed / 1000.0)
            if j % 10 == 0:
                set_all_pixels_rgbw(strip, 0, 0, 0, 255)
                strip.show()
                time.sleep(flash_duration)
                set_all_pixels_rgbw(strip, 0, 0, 0, 0)
                strip.show()
                time.sleep(flash_duration)

    run_generic_animation(strip, stop_event, update_function, update_speed=rainbow_speed)
