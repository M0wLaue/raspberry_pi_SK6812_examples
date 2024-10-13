# menu.py
import logging
from rpi_ws281x import Color

logger = logging.getLogger("SK6812Menu")

def options_menu(strip):
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