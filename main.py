# https://github.com/rpi-ws281x/rpi-ws281x-python
# sudo pip install rpi_ws281x
from rpi_ws281x import *
import time
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SK6812")

# LED strip configuration:
LED_COUNT      = 144     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.SK6812_STRIP_GRBW   # Strip type and colour ordering

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

def run_animation_1():
    logger.info("Running animation 1")
    RUN_COLORS = [
        (5, 0, 0),
        (0, 5, 0),
        (0, 0, 5),
        (5, 0, 0)
    ]

    l = strip.numPixels()
    lc = len(RUN_COLORS) - 1
    bl = l / lc

    logger.debug(f"Total number of pixels: {l}")
    logger.debug(f"Number of color blocks: {lc}")
    logger.debug(f"Block length: {bl}")

    try:
        for startPos in range(l):
            logger.debug(f"Start position: {startPos}")
            for i in range(l):
                relPos = (i - startPos) % bl
                block = int((i - startPos) // bl % lc)
                factors = (relPos * 1.0 / bl, (bl - relPos) * 1.0 / bl)

                red = RUN_COLORS[block + 1][0] * factors[0] + RUN_COLORS[block][0] * factors[1]
                green = RUN_COLORS[block + 1][1] * factors[0] + RUN_COLORS[block][1] * factors[1]
                blue = RUN_COLORS[block + 1][2] * factors[0] + RUN_COLORS[block][2] * factors[1]

                color = Color(int(red), int(green), int(blue))
                strip.setPixelColor(i, color)

            strip.show()
            time.sleep(50 / 1000.0)
    except KeyboardInterrupt:
        logger.info("Animation 1 interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in animation 1: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up and turning off LEDs after animation 1")
        for i in range(l):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

def run_animation_2():
    logger.info("Running animation 2 (Blinking all LEDs)")
    l = strip.numPixels()
    try:
        while True:
            # Turn all LEDs on (white)
            for i in range(l):
                strip.setPixelColor(i, Color(5, 5, 5))
            strip.show()
            time.sleep(0.5)

            # Turn all LEDs off
            for i in range(l):
                strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Animation 2 interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in animation 2: {e}", exc_info=True)
    finally:
        logger.info("Cleaning up and turning off LEDs after animation 2")
        for i in range(l):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

def main():
    logger.info("Starting LED animation selection menu")

    while True:
        print("Select an animation:")
        print("1: Running Colors Animation")
        print("2: Blinking All LEDs")
        print("0: Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_animation_1()
        elif choice == "2":
            run_animation_2()
        elif choice == "0":
            logger.info("Exiting program")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
