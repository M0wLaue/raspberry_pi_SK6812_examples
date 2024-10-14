import time
import logging
import math
import random
from .animation_utils import run_generic_animation, set_all_pixels, set_all_pixels_rgbw, clear_strip
from rpi_ws281x import Color
from threading import Event

logger = logging.getLogger("SK6812Animations")


def run_firework_animation(strip, stop_event: Event):
    logger.info("Running firework animation")
    l = strip.numPixels()

    def update_function(strip):
        firework_pos = random.randint(0, l - 1)
        color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for i in range(firework_pos - 3, firework_pos + 4):
            if 0 <= i < l:
                strip.setPixelColor(i, color)
        strip.show()
        for brightness in range(255, 0, -5):
            for i in range(firework_pos - 3, firework_pos + 4):
                if 0 <= i < l:
                    strip.setPixelColor(i, Color(
                        (color >> 16) * brightness // 255,
                        ((color >> 8) & 0xff) * brightness // 255,
                        (color & 0xff) * brightness // 255
                    ))
            strip.show()
            time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=random.uniform(500, 2000))


def run_cool_white_twinkle_animation(strip, stop_event: Event, twinkle_speed=100):
    logger.info("Running cool white twinkle animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            if random.random() > 0.5:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                strip.setPixelColorRGB(i, color[0], color[1], color[2], color[3])
            else:
                strip.setPixelColorRGB(i, 0, 0, 0, 0)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=twinkle_speed)


def run_lightning_storm_animation(strip, stop_event: Event, flash_duration=0.1):
    logger.info("Running lightning storm animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            strip.setPixelColorRGB(i, 0, 0, 50, 0)
        if random.random() < 0.05:
            for i in range(strip.numPixels()):
                strip.setPixelColorRGB(i, 255, 255, 255, 255)
            strip.show()
            time.sleep(flash_duration)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_strobe_effect(strip, stop_event: Event, strobe_duration=0.1, off_duration=0.1):
    logger.info("Running strobe effect")

    def update_function(strip):
        set_all_pixels_rgbw(strip, 255, 255, 255, 255)
        strip.show()
        time.sleep(strobe_duration)
        clear_strip(strip)
        strip.show()
        time.sleep(off_duration)

    run_generic_animation(strip, stop_event, update_function, update_speed=strobe_duration + off_duration)


def run_holiday_twinkle_animation(strip, stop_event: Event, speed=150):
    logger.info("Running holiday twinkle animation")
    colors = [(255, 0, 0, 0), (0, 255, 0, 0), (0, 0, 0, 255)]

    def update_function(strip):
        for i in range(strip.numPixels()):
            color = random.choice(colors)
            strip.setPixelColorRGB(i, color[0], color[1], color[2], color[3])
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_random_sparkles_animation(strip, stop_event: Event, speed=50):
    logger.info("Running random sparkles animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            if random.random() < 0.05:
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                white = random.randint(0, 255)
                strip.setPixelColorRGB(i, red, green, blue, white)
            else:
                strip.setPixelColorRGB(i, 0, 0, 0, 0)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_random_meteor_shower_animation(strip, stop_event: Event, meteor_size=10, decay=0.8, speed=50):
    logger.info("Running random meteor shower animation")

    def update_function(strip):
        start_pos = random.randint(0, strip.numPixels() - meteor_size)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for i in range(meteor_size):
            if start_pos + i < strip.numPixels():
                strip.setPixelColorRGB(start_pos + i, color[0], color[1], color[2], color[3])
        strip.show()
        for i in range(strip.numPixels()):
            prev_color = strip.getPixelColor(i)
            r = int(((prev_color >> 16) & 0xff) * decay)
            g = int(((prev_color >> 8) & 0xff) * decay)
            b = int((prev_color & 0xff) * decay)
            w = int(((prev_color >> 24) & 0xff) * decay)
            strip.setPixelColorRGB(i, r, g, b, w)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_random_white_strobes_animation(strip, stop_event: Event, flash_duration=0.1, speed=50):
    logger.info("Running random white strobes animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            if random.random() < 0.05:
                strip.setPixelColorRGB(i, 255, 255, 255, 255)
            else:
                strip.setPixelColorRGB(i, 0, 0, 0, 0)
        strip.show()
        time.sleep(flash_duration)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_random_color_shifts_animation(strip, stop_event: Event, speed=100):
    logger.info("Running random color shifts animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            white = random.randint(0, 255)
            strip.setPixelColorRGB(i, red, green, blue, white)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)


def run_random_walk_animation(strip, stop_event: Event, speed=100):
    logger.info("Running random walk animation")
    position = random.randint(0, strip.numPixels() - 1)

    def update_function(strip):
        nonlocal position
        position += random.choice([-1, 1])
        if position < 0:
            position = strip.numPixels() - 1
        elif position >= strip.numPixels():
            position = 0
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        white = random.randint(0, 255)
        strip.setPixelColorRGB(position, red, green, blue, white)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

def run_random_glitter_animation(strip, stop_event: Event, glitter_probability=0.1, speed=50):
    logger.info("Running random glitter animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            if random.random() < glitter_probability:
                red = random.randint(0, 255)
                green = random.randint(0, 255)
                blue = random.randint(0, 255)
                white = random.randint(0, 255)
                strip.setPixelColorRGB(i, red, green, blue, white)
            else:
                strip.setPixelColorRGB(i, 0, 0, 0, 0)
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

def run_comet_rain_animation(strip, stop_event: Event, comet_size=3, speed=100):
    logger.info("Running comet rain animation")

    def update_function(strip):
        clear_strip(strip)
        num_comets = random.randint(3, 6)  # Anzahl der gleichzeitig fallenden Kometen
        for _ in range(num_comets):
            start_pos = random.randint(0, strip.numPixels() - comet_size)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for i in range(comet_size):
                if start_pos + i < strip.numPixels():
                    strip.setPixelColorRGB(start_pos + i, color[0], color[1], color[2], color[3])
        strip.show()

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

def run_pixel_explosion_animation(strip, stop_event: Event, explosion_probability=0.05, speed=100):
    logger.info("Running pixel explosion animation")

    def update_function(strip):
        if random.random() < explosion_probability:
            center = random.randint(0, strip.numPixels() - 1)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for radius in range(1, strip.numPixels() // 2):
                if stop_event.is_set():
                    break
                for offset in [-radius, radius]:
                    if 0 <= center + offset < strip.numPixels():
                        strip.setPixelColorRGB(center + offset, color[0], color[1], color[2], color[3])
                strip.show()
                time.sleep(0.02)  # Kurze Pause zwischen den "Wellen"

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

def run_lava_explosion_animation(strip, stop_event: Event, speed=100):
    logger.info("Running lava explosion animation")

    def update_function(strip):
        center = random.randint(0, strip.numPixels() - 1)
        color = (255, random.randint(50, 150), 0, random.randint(0, 100))  # Lavafarben
        for radius in range(1, strip.numPixels() // 2):
            if stop_event.is_set():
                break
            for offset in [-radius, radius]:
                if 0 <= center + offset < strip.numPixels():
                    strip.setPixelColorRGB(center + offset, color[0], color[1], color[2], color[3])
            strip.show()
            time.sleep(0.05)  # Kurze Pause zwischen den "Wellen"

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)