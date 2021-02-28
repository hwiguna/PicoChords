
# Chords in CircuitPython by Hari Wiguna, 2021
# Resources:
# Learn:  https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/circuitpython
# Source: https://github.com/adafruit/Adafruit_CircuitPython_framebuf
# Docs: https://circuitpython.readthedocs.io/projects/ssd1306/en/latest/

import board
import busio
#import adafruit_framebuf
import adafruit_ssd1306
from analogio import AnalogIn
import math
import time

WIDTH, HEIGHT = 128, 64
x0, y0 = int(WIDTH/2), int(HEIGHT/2)

def SetupOLED():
	global oled
	i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
	oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=60)

def SetupUI():
	global rotPot, zoomPot, nodePot
	rotPot = AnalogIn(board.A1)
	zoomPot = AnalogIn(board.A0)
	nodePot = AnalogIn(board.A2)
	#moreNodeButton = DigitalInOut(board.GP13)
	#lessNodeButton = DigitalInOut(board.GP14)
	#moreNodeButton.pull = digitalio.Pull.UP
	#lessNodeButton.pull = digitalio.Pull.UP

def GetRotation():
	return  (65520 - rotPot.value) * 270 / 65520

def GetRadius():
	return  5 + int(zoomPot.value * (WIDTH*2) / 65520)

def GetNodeCount():
	return  3 + int(nodePot.value * 10 / 65520)

def DrawChord(rotDegrees, numNodes, radius):
	r = radius
	points = []
	rot = rotDegrees*2*math.pi/360
	for i in range(numNodes):
		a = rot+ (i * math.pi * 2 / numNodes)
		points.append( (int(x0 + math.sin(a)*r), int(y0 + math.cos(a)*r)) )

	oled.fill(0)
	for i in range(numNodes-1):
		for j in range(i, numNodes):
			oled.line(points[i][0], points[i][1], points[j][0], points[j][1], True)
	oled.show()

def DoChord():
	lastRotation, lastNumNodes, lastRadius = -1, -1,-1
	while True:
		numNodes = GetNodeCount()
		radius = GetRadius()
		newRotation = GetRotation()
		if numNodes!=lastNumNodes or abs(newRotation-lastRotation) > 4 or abs(radius-lastRadius)>2:
			DrawChord(newRotation, numNodes, radius)
			lastRotation = newRotation
			lastNumNodes = numNodes
			lastRadius = radius
		#time.sleep(.5)

def main():
	SetupOLED()
	SetupUI()
	DoChord()


