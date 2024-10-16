# menu.py
import logging
import pyaudio
from rpi_ws281x import Color

logger = logging.getLogger("SK6812Menu")

selected_audio_device = None  # Globale Variable zum Speichern des ausgewählten Aufnahmegeräts

def options_menu(strip):
    global selected_audio_device
    try:
        p = pyaudio.PyAudio()
        while True:
            print("Options Menu:")
            print("1: Set Brightness")
            print("2: Select Audio Input Device")
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
            elif choice == "2":
                print("Available Audio Input Devices:")
                for i in range(p.get_device_count()):
                    device_info = p.get_device_info_by_index(i)
                    if device_info["maxInputChannels"] > 0:
                        print(f"{i}: {device_info['name']}")
                try:
                    device_index = int(input("Enter the device index to use for audio input: "))
                    if 0 <= device_index < p.get_device_count():
                        selected_device = p.get_device_info_by_index(device_index)
                        if selected_device["maxInputChannels"] > 0:
                            selected_audio_device = selected_device
                            logger.info(f"Audio input device set to: {selected_device['name']}")
                            print(f"Audio input device set to: {selected_device['name']}")
                        else:
                            print("Selected device is not a valid input device.")
                    else:
                        print("Invalid device index.")
                except ValueError:
                    print("Invalid input. Please enter a valid device index.")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    except KeyboardInterrupt:
        logger.info("Options menu interrupted by user")
    finally:
        p.terminate()
