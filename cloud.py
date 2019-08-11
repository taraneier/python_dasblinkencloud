import math
import random
import opc
import time
import sys

numLEDs = 50
flashLimit = 8
flashFrequency = 80

debug = True
timefactor = 1000

if debug:
	timefactor = 100

# client = opc.Client('localhost:7890')
client = opc.Client('cloud:7890')
client.set_interpolation(True)

black = [(0, 0, 0)] * numLEDs
white = [(255, 255, 255)] * numLEDs
red = [(255, 0, 0)] * numLEDs


def main():
	print("Debug is {}, running with a timefactor of {}.".format(debug, 1/timefactor))

	# color_testing()
	# rainbow_cylon()
	sunrise()
	# test()
	# test_fillsolid()
	# lightning_rainbow()
	# lightning()


def color_testing():
	client.put_pixels(black)
	time.sleep(1)
	client.put_pixels(white)
	time.sleep(1)
	client.put_pixels(black)
	time.sleep(1)
	client.put_pixels(red)
	time.sleep(1)
	client.put_pixels(black)
	time.sleep(1)
	print("Red in hsv is (0,100,100)")
	print("Red in rgb is (255, 0, 0)")
	print("Red in hex is #FF0000")
	hsv = (0, 1, 1)
	print("hsv is {}".format(hsv))
	rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
	print("rgb is {}".format(rgb))
	hex = "#" + dec2hex(rgb[0]) + dec2hex(rgb[1]) + dec2hex(rgb[2])
	print("hex is {}".format(hex))
	fill_solid(0, numLEDs, rgb)

def test():
	for i in range(0, 200):
		print("i is {}".format(i))
		client.put_pixels(white)
		time.sleep(0.05)
		client.put_pixels(black)
		time.sleep(0.05)


def test_fillsolid():
	for i in range(0, 50):
		fill_solid(10, 15, (255, 0, 0))
		time.sleep(.1)
		fill_solid(10, 15, (0,0,0))
		time.sleep(.1)

def rainbow_cylon():
	for h in range(0, 255):

	# First slide the led in one direction
		for i in range(0, numLEDs):
			print("i is {} h is {}".format(i, h))
			fill_solid(i, 10, hsv_to_rgb(h, 1.0, 1.0))
			# time.sleep(.01)
		for i in range(numLEDs, 0):
			print("i is {} h is {}".format(i, h))
			fill_solid(i, 10, hsv_to_rgb(h, 1.0, 1.0))
			h = h - 1
			# time.sleep(.01)

	# time.sleep(.01)
			# Set the i'th led to red
			# leds[i] = CHSV(hue++, 255, 255);
			# thing = [(hue, hue, hue)] * numLEDs
			# print(thing)
			# Show the leds
			# client.put_pixels(thing)
			# now that we've shown the leds, reset the i'th led to black

	# 		client.put_pixels(black)
	# 		# // leds[i] = CRGB::Black;
	# 		# fadeall();
	# 		# // Wait a little bit before we loop around and do it again
	# 		# delay(10);
	# 		time.sleep(.1)
	# # hue = hue + 1
	fill_solid(0, numLEDs, (0,0,0))


def all(color):
	colorList = [(color)] * numLEDs
	client.put_pixels(colorList)



def sunrise():
	transition_time = 1
	client.put_pixels(black)
	# fade from black to red
	for v in range (0, 255):
		hsv = (0, 1.0, v/1.0/255)
		rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
		print("v is {}, hsv is {}, rgb is {} ".format(v, hsv, rgb))
		fill_solid(0, numLEDs, rgb)
		time.sleep(transition_time)
    # fade from red to orange
	for h in range(0, 60):
		hsv = (h, 1.0, v / 1.0 / 255)
		rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
		print("v is {}, hsv is {}, rgb is {} ".format(v, hsv, rgb))
		fill_solid(0, numLEDs, rgb)
		time.sleep(transition_time)
	client.put_pixels(white)
	time.sleep(transition_time)
	time.sleep(transition_time)


def lightning():
	client.put_pixels(black)
	ledstart = random.randint(0, numLEDs)  # Determine starting location of flash
	ledlen = random.randint(0, numLEDs - ledstart)  # // Determine length of flash (not to go beyond NUM_LEDS-1)
	flashes = random.randint(3, flashLimit)
	flashCounter = 0
	for flashCounter in range(0, flashes):
		print("flashcounter {} of flashes {}".format(flashCounter, flashes))
		if (flashCounter == 0):
			dimmer = 5  # the brightness of the leader is scaled down by a factor of 5
		else:
			dimmer = random.randint(1, 3)  # return strokes are brighter than the leader
		color = hsv_to_rgb(60, .1, 1 / dimmer)
		fill_solid(ledstart, ledlen, color)

		random_delay(3, 16)

		if (flashCounter == 0):
			time.sleep(.150)

		random_delay(0, 100, 50)

	client.put_pixels(black)
	random_delay(0, flashFrequency)


def lightning_rainbow():
	client.put_pixels(black)
	ledstart = random.randint(0, numLEDs)  # Determine starting location of flash
	ledlen = random.randint(0, numLEDs - ledstart)  # // Determine length of flash (not to go beyond NUM_LEDS-1)
	flashes = random.randint(3, flashLimit)
	flashCounter = 0
	for flashCounter in range(0, flashes):
		print("flashcounter {} of flashes {}".format(flashCounter, flashes))
		if (flashCounter == 0):
			dimmer = 5  # the brightness of the leader is scaled down by a factor of 5
		else:
			dimmer = random.randint(1, 3)  # return strokes are brighter than the leader

		color = hsv_to_rgb(random.randint(0, 255), 1, 1 / dimmer)
		fill_solid(ledstart, ledlen, color)
		random_delay(3, 16)
		if (flashCounter == 0):
			time.sleep(.150)
		random_delay(0, 100, 50)

	client.put_pixels(black)
	random_delay(0, flashFrequency)


def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def dec2hex(d):
    """return a two character hexadecimal string representation of integer d"""
    return "%02X" % d

def fill_solid(ledstart, ledlen, color):
	if debug:
		print("color is {}".format(color))
	# hex = (dec2hex(color[0]), dec2hex(color[1]), dec2hex(color[2]))
	# print("hex is {}".format(hex))
	first = [(0, 0, 0)] * ledstart
	middle = [color] * ledlen
	last = [(0, 0, 0)] * (numLEDs - ledstart - ledlen)
	strip = first + middle + last
	client.put_pixels(strip)


def random_delay(min, max, base = 0):
	waiting = (base + random.randint(min, max) )/ timefactor
	if debug:
		print("Waiting {} seconds.".format(waiting))
	time.sleep(waiting)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print('Interrupted')
		client.put_pixels(black)
		sys.exit(0)
