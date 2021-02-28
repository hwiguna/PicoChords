# Resources:
# Learn:  https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/circuitpython
# Source: https://github.com/adafruit/Adafruit_CircuitPython_framebuf

import board
import busio
import adafruit_framebuf
import adafruit_ssd1306

WIDTH, HEIGHT = 128, 64

def SetupOLED():
	global oled
	i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
	oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=60)

def TestOLED():
	oled.fill(0)
	oled.pixel(64,32,1)
	oled.text("Hello", 0,0, True) # Requires font5x8.bin to be in root of CIRCUITPYTHON drive
	oled.show()

def main():
	print("Begin main...")
	SetupOLED()
	TestOLED()

