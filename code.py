"""CircuitPython Essentials NeoPixel RGBW example"""
import time
import board
import neopixel
import digitalio
import random

pixel_pin = board.A1
num_pixels = 24

# vibration sensor
motion_pin = board.D0  # Pin where vibration switch is connected
pin = digitalio.DigitalInOut(motion_pin)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
vibration = False


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=(1, 0, 2, 3))


def vibration_detector():
    while True:
        if not pin.value:
            return True


def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)

def blinker():
    for i in range(5):
        pixels[0] = (0, 255, 255, 0)
        pixels.show()
        time.sleep(0.6)
        pixels[0] = (180, 0, 255, 0)
        pixels.show()
        time.sleep(0.6)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
        ramping_up = False

RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
BLACK = (0, 0, 0, 0)

while True:

    if vibration_detector():
        rancase = random.randint(1, 4)

        if rancase == 1:
            color_chase(GREEN,0.1)
            color_chase(BLACK,0.1)
        elif rancase == 2:
            color_chase(PURPLE,0.1)
            color_chase(BLACK,0.1)
        elif rancase == 3:
            rainbow_cycle(0)
            color_chase(BLACK,0.1)
        elif rancase == 4:
            blinker()
            color_chase(BLACK,0.1)

