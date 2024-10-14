import time
import logging
import math
import random
from .animation_utils import run_generic_animation, set_all_pixels, set_all_pixels_rgbw, clear_strip
from rpi_ws281x import Color
from threading import Event

logger = logging.getLogger("SK6812Animations")


def run_fade_animation(strip, stop_event: Event):
    logger.info("Running fade animation")
    colors = [
        (255, 0, 0),  # Rot
        (0, 255, 0),  # Grün
        (0, 0, 255)   # Blau
    ]

    def update_function(strip):
        for color in colors:
            for brightness in range(0, 256, 5):  # Von dunkel zu hell
                if stop_event.is_set():
                    return
                set_all_pixels(strip, Color(color[0] * brightness // 255, color[1] * brightness // 255, color[2] * brightness // 255))
                strip.show()
                time.sleep(0.05)
            for brightness in range(255, -1, -5):  # Von hell zu dunkel
                if stop_event.is_set():
                    return
                set_all_pixels(strip, Color(color[0] * brightness // 255, color[1] * brightness // 255, color[2] * brightness // 255))
                strip.show()
                time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_theater_chase_animation(strip, stop_event: Event, color=Color(127, 127, 127), wait_ms=50):
    logger.info("Running theater chase animation")
    l = strip.numPixels()

    def update_function(strip):
        for q in range(3):
            if stop_event.is_set():
                return
            for i in range(0, l, 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, l, 3):
                strip.setPixelColor(i + q, 0)

    run_generic_animation(strip, stop_event, update_function, update_speed=wait_ms)


def run_twinkle_animation(strip, stop_event: Event):
    logger.info("Running twinkle animation")
    l = strip.numPixels()

    def update_function(strip):
        for i in range(l):
            if stop_event.is_set():
                return
            # Zufällige Farbe für jeden Pixel
            color = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.05)
        for i in range(l):
            if stop_event.is_set():
                return
            if random.random() > 0.5:
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_wave_animation(strip, stop_event: Event, wave_speed=0.1, color=Color(0, 0, 255)):
    logger.info("Running wave animation")
    l = strip.numPixels()

    def update_function(strip):
        for i in range(l):
            if stop_event.is_set():
                return
            # Erzeugt eine Sinuswelle für die Farbintensität
            intensity = int((math.sin(i * wave_speed) + 1) * 127)
            strip.setPixelColor(i, Color(intensity, 0, 255 - intensity))

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_meteor_animation(strip, stop_event: Event, meteor_size=10, decay=0.8):
    logger.info("Running meteor animation")
    l = strip.numPixels()

    def update_function(strip):
        for start_pos in range(l):
            if stop_event.is_set():
                return
            # Erzeuge den Meteor
            for i in range(meteor_size):
                if start_pos + i < l:
                    strip.setPixelColor(start_pos + i, Color(255, 255, 255))
            strip.show()
            time.sleep(50 / 1000.0)
            # Verblasse den Meteor
            for i in range(l):
                color = strip.getPixelColor(i)
                r = int(((color >> 16) & 0xff) * decay)
                g = int(((color >> 8) & 0xff) * decay)
                b = int((color & 0xff) * decay)
                strip.setPixelColor(i, Color(r, g, b))

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_larson_scanner_animation(strip, stop_event: Event, color=Color(255, 0, 0), tail_length=5, decay=0.6):
    logger.info("Running Larson Scanner animation")
    l = strip.numPixels()

    def update_function(strip):
        # Gehe vorwärts durch die LEDs
        for i in range(l):
            if stop_event.is_set():
                return
            strip.setPixelColor(i, color)
            # Lasse die vorherigen LEDs verblassen, um einen "Schweif" zu erzeugen
            for j in range(1, tail_length + 1):
                if i - j >= 0:
                    prev_color = strip.getPixelColor(i - j)
                    r = int(((prev_color >> 16) & 0xff) * decay)
                    g = int(((prev_color >> 8) & 0xff) * decay)
                    b = int((prev_color & 0xff) * decay)
                    strip.setPixelColor(i - j, Color(r, g, b))
            strip.show()
            time.sleep(0.05)
        # Gehe rückwärts durch die LEDs
        for i in range(l - 1, -1, -1):
            if stop_event.is_set():
                return
            strip.setPixelColor(i, color)
            for j in range(1, tail_length + 1):
                if i + j < l:
                    prev_color = strip.getPixelColor(i + j)
                    r = int(((prev_color >> 16) & 0xff) * decay)
                    g = int(((prev_color >> 8) & 0xff) * decay)
                    b = int((prev_color & 0xff) * decay)
                    strip.setPixelColor(i + j, Color(r, g, b))
            strip.show()
            time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_comet_animation(strip, stop_event: Event, color=Color(0, 0, 255), tail_length=10, decay=0.9):
    logger.info("Running comet animation")
    l = strip.numPixels()

    def update_function(strip):
        for start_pos in range(l):
            if stop_event.is_set():
                return
            # Setze die Kometen-Lichtspitze
            strip.setPixelColor(start_pos, color)
            # Erzeuge den Kometen-Schweif, der langsam verblasst
            for i in range(1, tail_length + 1):
                if start_pos - i >= 0:
                    tail_color = strip.getPixelColor(start_pos - i)
                    r = int(((tail_color >> 16) & 0xff) * decay)
                    g = int(((tail_color >> 8) & 0xff) * decay)
                    b = int((tail_color & 0xff) * decay)
                    strip.setPixelColor(start_pos - i, Color(r, g, b))
            strip.show()
            time.sleep(0.05)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)

def run_bouncing_balls_animation(strip, stop_event: Event, num_balls=3, ball_colors=[Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]):
    logger.info("Running bouncing balls animation")
    l = strip.numPixels()

    positions = [0] * num_balls
    velocities = [random.uniform(0.2, 0.8) for _ in range(num_balls)]

    def update_function(strip):
        for i in range(num_balls):
            positions[i] += velocities[i]
            if positions[i] >= l - 1 or positions[i] <= 0:
                velocities[i] *= -1
        clear_strip(strip)
        for i in range(num_balls):
            strip.setPixelColor(int(positions[i]), ball_colors[i])

    run_generic_animation(strip, stop_event, update_function, update_speed=50)


def run_white_comet_animation(strip, stop_event: Event, comet_size=5, comet_color=Color(0, 0, 255, 255), tail_decay=0.8):
    logger.info("Running white comet animation")
    l = strip.numPixels()

    def update_function(strip):
        for start_pos in range(l):
            if stop_event.is_set():
                return
            strip.setPixelColorRGB(start_pos, 0, 0, 255, 255)
            for i in range(1, comet_size + 1):
                if start_pos - i >= 0:
                    tail_color = strip.getPixelColor(start_pos - i)
                    r = int(((tail_color >> 16) & 0xff) * tail_decay)
                    g = int(((tail_color >> 8) & 0xff) * tail_decay)
                    b = int((tail_color & 0xff) * tail_decay)
                    w = int(((tail_color >> 24) & 0xff) * tail_decay)
                    strip.setPixelColorRGB(start_pos - i, r, g, b, w)
            strip.show()
            time.sleep(50 / 1000.0)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)

def run_fireplace_animation(strip, stop_event: Event):
    logger.info("Running fireplace animation")

    def update_function(strip):
        for i in range(strip.numPixels()):
            if stop_event.is_set():
                return
            red = random.randint(200, 255)
            green = random.randint(50, 150)
            blue = random.randint(0, 50)
            white = random.randint(0, 50)
            strip.setPixelColorRGB(i, red, green, blue, white)

    run_generic_animation(strip, stop_event, update_function, update_speed=50)

def run_aurora_borealis_animation(strip, stop_event: Event, speed=100):
    logger.info("Running aurora borealis animation")
    colors = [
        (0, 64, 255, 0),  # Blau
        (0, 128, 0, 64),  # Grün
        (128, 0, 255, 0),  # Violett
        (0, 64, 128, 128)  # Mischung
    ]

    def update_function(strip):
        for i in range(strip.numPixels()):
            color = random.choice(colors)
            strip.setPixelColorRGB(i, color[0], color[1], color[2], color[3])
        strip.show()
        time.sleep(speed / 1000.0)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

