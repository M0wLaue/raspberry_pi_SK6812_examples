# sound_animations.py
import time
import logging
import numpy as np
import pyaudio
from collections import deque
from .animation_utils import run_generic_animation
from rpi_ws281x import Color
from threading import Event

def run_music_synchronized_wave(strip, stop_event: Event, selected_audio_device, speed=10, chunk=2048, rate=44100, max_window_size=10, scaling="exponential", **kwargs):
    logger = logging.getLogger("SK6812Animations")
    logger.info("Running music synchronized wave animation")

    # Setup PyAudio for capturing microphone input
    p = pyaudio.PyAudio()
    input_device_index = selected_audio_device['index'] if selected_audio_device else None
    # logger.debug(f"Audio device:[{selected_audio_device['index']}]: {selected_audio_device['name']}")

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=chunk)
    
    if stream.is_active():
        logger.info("Audio stream successfully initialized.")
    else:
        logger.error("Audio stream initialization failed.")

    # Ringpuffer für das "Windowed Maximum"
    max_values_window = deque(maxlen=max_window_size)

    def update_function(strip):
        try:
            # Read data from microphone
            data = np.frombuffer(stream.read(chunk, exception_on_overflow=False), dtype=np.int16)
            fft_data = np.abs(np.fft.rfft(data))

            # Skalierung der Frequenzbins
            if scaling == "logarithmic":
                # Logarithmische Skalierung der Frequenzbins
                log_indices = np.logspace(0, np.log10(len(fft_data)), num=strip.numPixels(), base=10, dtype=int)
                log_indices = np.clip(log_indices, 0, len(fft_data) - 1)  # Ensure indices are within bounds
                fft_data = fft_data[log_indices]
            elif scaling == "exponential":
                # Exponentielle Skalierung der Frequenzbins
                exp_indices = np.unique(np.round(np.geomspace(1, len(fft_data), num=strip.numPixels())).astype(int))
                exp_indices = np.clip(exp_indices, 0, len(fft_data) - 1)  # Ensure indices are within bounds
                fft_data = fft_data[exp_indices]
            else:
                # Lineare Skalierung (Standard)
                fft_data = fft_data[:strip.numPixels()]

            # Falls die Anzahl der FFT-Werte nicht mit der Anzahl der LEDs übereinstimmt, passe sie an
            if len(fft_data) < strip.numPixels():
                fft_data = np.pad(fft_data, (0, strip.numPixels() - len(fft_data)), 'constant')
            elif len(fft_data) > strip.numPixels():
                fft_data = fft_data[:strip.numPixels()]

            # Berechnung des aktuellen Maximums und Aktualisierung des Ringpuffers
            current_max_fft = np.max(fft_data) if np.max(fft_data) > 0 else 1
            max_values_window.append(current_max_fft)

            # Verwende das größte Maximum aus dem Fenster für die Normalisierung
            window_max_fft = max(max_values_window)

            # Normalize FFT data to fit LED strip
            normalized_data = (fft_data / window_max_fft) * 255

            # Set colors based on frequency range
            for i in range(strip.numPixels()):
                intensity = int(normalized_data[i])
                if i < strip.numPixels() // 3:
                    # Low frequencies - Red
                    strip.setPixelColorRGB(i, intensity, 0, 0, 0)
                elif i < 2 * strip.numPixels() // 3:
                    # Mid frequencies - Green
                    strip.setPixelColorRGB(i, 0, intensity, 0, 0)
                else:
                    # High frequencies - Blue
                    strip.setPixelColorRGB(i, 0, 0, intensity, 0)
            strip.show()

        except IOError as e:
            logger.warning(f"Audio input overflowed: {e}")
        except Exception as e:
            logger.error(f"Error in update_function: {e}", exc_info=True)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

    # Cleanup PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def run_frequency_bands_gradient(strip, stop_event: Event, selected_audio_device, speed=10, chunk=2048, rate=44100, max_window_size=10, scaling="logarithmic", **kwargs):
    logger = logging.getLogger("SK6812Animations")
    logger.info("Running frequency bands and color gradient animation")

    # Setup PyAudio for capturing microphone input
    p = pyaudio.PyAudio()
    input_device_index = selected_audio_device['index'] if selected_audio_device else 0
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=chunk)
    
    if stream.is_active():
        logger.info("Audio stream successfully initialized.")
    else:
        logger.error("Audio stream initialization failed.")

    # Ring buffer for the "Windowed Maximum"
    max_values_window = deque(maxlen=max_window_size)

    def update_function(strip):
        try:
            # Read data from microphone
            data = np.frombuffer(stream.read(chunk, exception_on_overflow=False), dtype=np.int16)
            fft_data = np.abs(np.fft.rfft(data))

            # Frequency bin scaling
            if scaling == "logarithmic":
                log_indices = np.logspace(0, np.log10(len(fft_data)), num=strip.numPixels(), base=10, dtype=int)
                log_indices = np.clip(log_indices, 0, len(fft_data) - 1)
                fft_data = fft_data[log_indices]
            elif scaling == "exponential":
                exp_indices = np.unique(np.round(np.geomspace(1, len(fft_data), num=strip.numPixels())).astype(int))
                exp_indices = np.clip(exp_indices, 0, len(fft_data) - 1)
                fft_data = fft_data[exp_indices]
            else:
                fft_data = fft_data[:strip.numPixels()]

            if len(fft_data) < strip.numPixels():
                fft_data = np.pad(fft_data, (0, strip.numPixels() - len(fft_data)), 'constant')
            elif len(fft_data) > strip.numPixels():
                fft_data = fft_data[:strip.numPixels()]

            # Update the windowed maximum buffer
            current_max_fft = np.max(fft_data) if np.max(fft_data) > 0 else 1
            max_values_window.append(current_max_fft)
            window_max_fft = max(max_values_window)

            # Normalize FFT data to fit LED strip
            normalized_data = (fft_data / window_max_fft) * 255

            # Apply gradient color based on frequency bins
            for i in range(strip.numPixels()):
                intensity = int(normalized_data[i])
                hue = int((i / strip.numPixels()) * 255)  # Create a gradient hue from 0 to 255
                red = intensity if hue < 85 else 0
                green = intensity if 85 <= hue < 170 else 0
                blue = intensity if hue >= 170 else 0
                color = Color(red, green, blue)
                strip.setPixelColor(i, color)
            strip.show()

        except IOError as e:
            logger.warning(f"Audio input overflowed: {e}")
        except Exception as e:
            logger.error(f"Error in update_function: {e}", exc_info=True)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

    # Cleanup PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def run_beat_pulse_animation(strip, stop_event: Event, selected_audio_device, speed=10, chunk=2048, rate=44100, max_window_size=50, threshold=1.3, **kwargs):
    logger = logging.getLogger("SK6812Animations")
    logger.info("Running beat pulse animation")

    # Setup PyAudio for capturing microphone input
    p = pyaudio.PyAudio()
    input_device_index = selected_audio_device['index'] if selected_audio_device else 0
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=chunk)
    
    if stream.is_active():
        logger.info("Audio stream successfully initialized.")
    else:
        logger.error("Audio stream initialization failed.")

    # Variables to track beat detection
    max_values_window = deque(maxlen=max_window_size)  # Use a sliding window to track recent max values
    beat_detected = False
    color_index = 0
    colors = [
        Color(255, 0, 0),  # Red
        Color(0, 255, 0),  # Green
        Color(0, 0, 255),  # Blue
        Color(255, 255, 0),  # Yellow
        Color(0, 255, 255),  # Cyan
        Color(255, 0, 255),  # Magenta
        Color(255, 255, 255)  # White
    ]

    def update_function(strip):
        nonlocal beat_detected, color_index
        try:
            # Read data from microphone
            data = np.frombuffer(stream.read(chunk, exception_on_overflow=False), dtype=np.int16)
            fft_data = np.abs(np.fft.rfft(data))
            current_max_fft = np.max(fft_data) if np.max(fft_data) > 0 else 1

            # Update the sliding window with the current max value
            max_values_window.append(current_max_fft)
            window_average = np.mean(max_values_window)

            # Detect a beat if the current max is significantly higher than the window average
            if current_max_fft > threshold * window_average and not beat_detected:
                beat_detected = True
                color_index = (color_index + 1) % len(colors)  # Cycle through colors
                logger.debug(f"Beat detected! Switching to color index {color_index}")
            elif current_max_fft < window_average:
                beat_detected = False

            # Set all LEDs to the current color with a pulsing effect
            intensity = int((current_max_fft / window_average) * 255)
            intensity = min(max(intensity, 0), 255)  # Clamp intensity between 0 and 255
            color = colors[color_index]
            adjusted_color = Color(
                (color >> 16 & 0xff) * intensity // 255,
                (color >> 8 & 0xff) * intensity // 255,
                (color & 0xff) * intensity // 255,
                (color >> 24 & 0xff) * intensity // 255
            )
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, adjusted_color)
            strip.show()

        except IOError as e:
            logger.warning(f"Audio input overflowed: {e}")
        except Exception as e:
            logger.error(f"Error in update_function: {e}", exc_info=True)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

    # Cleanup PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

def run_wave_ripple_effect(strip, stop_event: Event, selected_audio_device, speed=5, chunk=2048, rate=44100, max_window_size=100, color_boost=1.2, frequency_bin_factor=5, **kwargs):
    logger = logging.getLogger("SK6812Animations")
    logger.info("Running wave ripple effect animation")

    # Setup PyAudio for capturing microphone input
    p = pyaudio.PyAudio()
    input_device_index = selected_audio_device['index'] if selected_audio_device else 0

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=chunk)

    if stream.is_active():
        logger.info("Audio stream successfully initialized.")
    else:
        logger.error("Audio stream initialization failed.")

    # Ring buffer for the "Windowed Maximum"
    max_values_window = deque(maxlen=max_window_size)
    ripple_queue = deque(maxlen=50)  # Reduced length to make the ripple effect more noticeable

    def update_function(strip):
        try:
            # Read data from microphone
            data = np.frombuffer(stream.read(chunk, exception_on_overflow=False), dtype=np.int16)
            fft_data = np.abs(np.fft.rfft(data))
            current_max_fft = np.max(fft_data) if np.max(fft_data) > 0 else 1
            max_values_window.append(current_max_fft)
            window_max_fft = max(max_values_window)
            normalized_volume = current_max_fft / window_max_fft

            # Find the dominant frequency bin
            dominant_frequency_index = np.argmax(fft_data)
            frequency_bin = ((dominant_frequency_index / len(fft_data)) * rate / 2) * frequency_bin_factor

            # Determine color based on frequency with smooth transitions
            red, green, blue = 0, 0, 0

            if frequency_bin < rate / 6:
                # Low frequencies (Red to Yellow)
                red = 255
                green = int((frequency_bin / (rate / 6)) * 255 * color_boost)
            elif frequency_bin < rate / 3:
                # Mid frequencies (Yellow to Green to Cyan)
                green = 255
                red = int(((rate / 3 - frequency_bin) / (rate / 6)) * 255 * color_boost)
                blue = int(((frequency_bin - rate / 6) / (rate / 6)) * 255 * color_boost)
            else:
                # High frequencies (Cyan to Blue)
                blue = 255
                green = int(((rate / 2 - frequency_bin) / (rate / 3)) * 255 * color_boost)

            # Add white component based on volume
            white_component = int(normalized_volume * 255 / color_boost)
            color = (min(255, red + white_component),
                     min(255, green + white_component),
                     min(255, blue + white_component),
                     white_component)

            # Add new ripple to the queue
            ripple_queue.append((0, color, normalized_volume))

            # Update ripples
            for index, (position, color, volume) in enumerate(ripple_queue):
                ripple_queue[index] = (position + int(3 * volume), color, volume)  # High volume ripples move faster

            # Render ripples on the LED strip
            for i in range(strip.numPixels()):
                intensity = 0
                final_color = (0, 0, 0, 0)

                for position, ripple_color, volume in ripple_queue:
                    distance = abs(i - position)
                    if distance < strip.numPixels() // 2:  # Reduced distance to make ripple endings more visible
                        ripple_intensity = max(255 - (distance * 4), 0)  # Reduce intensity with distance, slower decay
                        if ripple_intensity > intensity:
                            intensity = ripple_intensity
                            final_color = ripple_color

                # Set the color with intensity modulation
                strip.setPixelColor(i, Color(
                    int(final_color[0] * intensity / 255),
                    int(final_color[1] * intensity / 255),
                    int(final_color[2] * intensity / 255),
                    int(final_color[3] * intensity / 255),
                ))

            strip.show()

        except IOError as e:
            logger.warning(f"Audio input overflowed: {e}")
        except Exception as e:
            logger.error(f"Error in update_function: {e}", exc_info=True)

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

    # Cleanup PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()