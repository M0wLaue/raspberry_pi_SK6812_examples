# sound_animations.py
import time
import logging
import numpy as np
import pyaudio
from collections import deque
from .animation_utils import run_generic_animation
from rpi_ws281x import Color
from threading import Event

def run_music_synchronized_wave(strip, stop_event: Event, selected_audio_device, speed=10, chunk=2048, rate=44100, max_window_size=10, scaling="linear", **kwargs):
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
