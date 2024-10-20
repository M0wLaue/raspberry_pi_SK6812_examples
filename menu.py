# menu.py
import logging
import pyaudio
from rpi_ws281x import Color
from settings import SettingsManager

logger = logging.getLogger("SK6812Menu")

# Lade die zentrale Einstellungsinstanz
settings = SettingsManager.get_instance()

def options_menu(strip):
    try:
        p = pyaudio.PyAudio()
        while True:
            print("Options Menu:")
            print("1: Set Brightness")
            if p.get_device_count() > 0:
                print("2: Select Audio Input Device")
            else:
                print("2: No Audio Devices Available")
            print("3: Set Animation Parameters")
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
                if p.get_device_count() == 0:
                    print("No audio devices available.")
                    continue
                print("Available Audio Input Devices:")
                for i in range(p.get_device_count()):
                    device_info = p.get_device_info_by_index(i)
                    if device_info["maxInputChannels"] > 0:
                        print(f"{i}: {device_info['name']} - Max Input Channels: {device_info['maxInputChannels']}")
                try:
                    device_index = int(input("Enter the device index to use for audio input: "))
                    if 0 <= device_index < p.get_device_count():
                        selected_device = p.get_device_info_by_index(device_index)
                        if selected_device["maxInputChannels"] > 0:
                            settings.selected_audio_device = selected_device
                            logger.info(f"Audio input device set to: {selected_device['name']}")
                            print(f"Audio input device set to: {selected_device['name']}")
                        else:
                            print("Selected device is not a valid input device.")
                    else:
                        print("Invalid device index.")
                except ValueError:
                    print("Invalid input. Please enter a valid device index.")
            elif choice == "3":
                # Animation Parameter Menü
                animation_settings = settings.animation_settings
                print("Animation Parameter Settings:")
                print(f"1: Speed (current: {animation_settings.speed})")
                print(f"2: Meteor Size (current: {animation_settings.meteor_size})")
                print(f"3: Decay (current: {animation_settings.decay})")
                print(f"4: Tail Length (current: {animation_settings.tail_length})")
                print(f"5: Glitter Probability (current: {animation_settings.glitter_probability})")
                # ... füge weitere Parameter hinzu
                param_choice = input("Enter the parameter to change: ")

                try:
                    if param_choice == "1":
                        animation_settings.speed = int(input("Enter new speed: "))
                    elif param_choice == "2":
                        animation_settings.meteor_size = int(input("Enter new meteor size: "))
                    elif param_choice == "3":
                        animation_settings.decay = float(input("Enter new decay (0.0 - 1.0): "))
                    elif param_choice == "4":
                        animation_settings.tail_length = int(input("Enter new tail length: "))
                    elif param_choice == "5":
                        animation_settings.glitter_probability = float(input("Enter new glitter probability (0.0 - 1.0): "))
                    # ... weitere Abfragen für andere Parameter
                except ValueError:
                    print("Invalid input. Please enter the correct value type.")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    except KeyboardInterrupt:
        logger.info("Options menu interrupted by user")
    finally:
        p.terminate()
