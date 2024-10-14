# animation_utils.py

from rpi_ws281x import Color
import time
import logging

class RGBColor:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def to_color(self):
        return Color(self.r, self.g, self.b)

    @staticmethod
    def from_tuple(color_tuple):
        return RGBColor(color_tuple[0], color_tuple[1], color_tuple[2])

def run_generic_animation(strip, stop_event, update_function, update_speed=50, **kwargs):
    """
    Führt eine generische Animation aus, die eine update_function verwendet.
    
    :param strip: Der LED-Streifen (PixelStrip oder Adafruit_NeoPixel)
    :param stop_event: threading.Event-Objekt, das das Ende der Animation signalisiert
    :param update_function: Funktion, die pro Frame ausgeführt wird und die LED-Werte festlegt
    :param update_speed: Zeitverzögerung zwischen den Aktualisierungen in Millisekunden
    :param **kwargs: Zusätzliche Argumente, die an die update_function übergeben werden
    """
    logger = logging.getLogger("GenericAnimation")
    
    try:
        while not stop_event.is_set():
            # Update-Funktion aufrufen, um die LEDs zu aktualisieren
            update_function(strip, **kwargs)
            
            # Zeige die Änderungen auf dem LED-Streifen
            strip.show()
            
            # Warte zwischen den Updates
            time.sleep(update_speed / 1000.0)
    except Exception as e:
        logger.error(f"Error in generic animation: {e}", exc_info=True)
    finally:
        # Streifen löschen, wenn die Animation beendet ist
        clear_strip(strip)


def clear_strip(strip):
    """Schaltet alle LEDs aus, indem sie auf Schwarz (0, 0, 0) gesetzt werden."""
    set_all_pixels(strip, Color(0, 0, 0))

def set_all_pixels(strip, color):
    """Setzt alle LEDs im Streifen auf dieselbe Farbe."""
    l = strip.numPixels()
    for i in range(l):
        strip.setPixelColor(i, color)
    strip.show()

def set_all_pixels_rgbw(strip, red, green, blue, white):
    """Setzt alle LEDs auf den gleichen RGBW-Wert."""
    l = strip.numPixels()
    for i in range(l):
        strip.setPixelColorRGB(i, red, green, blue, white)
    strip.show()

def fade_color(color, brightness):
    """
    Skaliert eine Farbe nach einem Helligkeitswert. Der Helligkeitswert sollte zwischen 0 und 255 liegen.
    Die Funktion gibt eine neue Farbe zurück, die in allen Komponenten (R, G, B, W) skaliert wurde.
    """
    r = (color >> 16) & 0xff
    g = (color >> 8) & 0xff
    b = color & 0xff
    w = (color >> 24) & 0xff
    return Color(
        r * brightness // 255,
        g * brightness // 255,
        b * brightness // 255,
        w * brightness // 255
    )

def wheel_rgbw(pos):
    """
    Erzeugt eine Farbverlauf-Funktion für Regenbogenfarben. Pos sollte ein Wert zwischen 0 und 255 sein.
    Gibt eine RGBW-Farbe zurück.
    """
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0, 0)  # Kein Weiß in der Regenbogenfarbe
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3, 0)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3, 0)

def scale_color(color, scale_factor):
    """
    Skaliert eine Farbe nach einem Skalierungsfaktor. Der Faktor sollte zwischen 0 und 1 liegen.
    Diese Funktion wird verwendet, um eine Farbe gleichmäßig zu dimmen oder aufzuhellen.
    """
    r = (color >> 16) & 0xff
    g = (color >> 8) & 0xff
    b = color & 0xff
    w = (color >> 24) & 0xff
    return Color(
        int(r * scale_factor),
        int(g * scale_factor),
        int(b * scale_factor),
        int(w * scale_factor)
    )

def random_color():
    """Erzeugt eine zufällige RGBW-Farbe."""
    import random
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

def random_rgb_color():
    """Erzeugt eine zufällige RGB-Farbe ohne Weißanteil."""
    import random
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        0
    )

def blend_colors(color1, color2, ratio):
    """
    Mischt zwei Farben basierend auf einem Verhältnis (ratio). Ratio sollte zwischen 0 und 1 liegen.
    Gibt eine neue gemischte Farbe zurück.
    """
    r1, g1, b1, w1 = (color1 >> 16) & 0xff, (color1 >> 8) & 0xff, color1 & 0xff, (color1 >> 24) & 0xff
    r2, g2, b2, w2 = (color2 >> 16) & 0xff, (color2 >> 8) & 0xff, color2 & 0xff, (color2 >> 24) & 0xff

    r = int(r1 * (1 - ratio) + r2 * ratio)
    g = int(g1 * (1 - ratio) + g2 * ratio)
    b = int(b1 * (1 - ratio) + b2 * ratio)
    w = int(w1 * (1 - ratio) + w2 * ratio)

    return Color(r, g, b, w)
