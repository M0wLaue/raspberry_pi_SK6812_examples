# sound_animations.py
import time
import logging
import numpy as np
import pyaudio
from .animation_utils import run_generic_animation
from rpi_ws281x import Color
from threading import Event

logger = logging.getLogger("SK6812Animations")

def run_music_synchronized_wave(strip, stop_event: Event, selected_audio_device, speed=50, chunk=1024, rate=44100):
    logger.info("Running music synchronized wave animation")

    # Setup PyAudio for capturing microphone input
    p = pyaudio.PyAudio()
    input_device_index = selected_audio_device['index'] if selected_audio_device else None

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    input_device_index=input_device_index,
                    frames_per_buffer=chunk)

    def update_function(strip):
        # Read data from microphone
        data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        fft_data = np.abs(np.fft.rfft(data))
        fft_data = fft_data[:strip.numPixels()]

        # Normalize FFT data to fit LED strip
        max_fft = np.max(fft_data) if np.max(fft_data) > 0 else 1
        normalized_data = (fft_data / max_fft) * 255

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

    run_generic_animation(strip, stop_event, update_function, update_speed=speed)

    # Cleanup PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()