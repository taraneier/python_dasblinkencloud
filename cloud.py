import math
import random
import opc
import time
import sys

debug = False


class Cloud:
    def __init__(self):

        self.numleds = 50
        self.flashLimit = 8
        self.flashFrequency = 80
        self.timefactor = 1000

        self.programs = [
            'sunrise',
            'color_testing',
            'rainbow_cylon',
            'test',
            'test_fillsolid',
            'lightning_rainbow',
            'lightning'
        ]

        if debug:
            self.timefactor = 100

        # client = opc.Client('localhost:7890')
        self.client = opc.Client('cloud:7890')
        self.client.set_interpolation(True)

        self.black = [(0, 0, 0)] * self.numleds
        self.white = [(255, 255, 255)] * self.numleds
        self.red = [(255, 0, 0)] * self.numleds

    def get_programs(self):
        return self.programs

    def color_testing(self):
        self.client.put_pixels(self.black)
        time.sleep(1)
        self.client.put_pixels(self.white)
        time.sleep(1)
        self.client.put_pixels(self.black)
        time.sleep(1)
        self.client.put_pixels(self.red)
        time.sleep(1)
        self.client.put_pixels(self.black)
        time.sleep(1)
        print("Red in hsv is (0,100,100)")
        print("Red in rgb is (255, 0, 0)")
        print("Red in hex is #FF0000")
        hsv = (0, 1, 1)
        if debug:
            print("hsv is {}".format(hsv))
        rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        if debug:
            print("rgb is {}".format(rgb))
        hex_val = "#" + dec2hex(rgb[0]) + dec2hex(rgb[1]) + dec2hex(rgb[2])
        if debug:
            print("hex is {}".format(hex_val))
        self.fill_solid(0, self.numleds, rgb)

    def test(self):
        for i in range(0, 200):
            print("i is {}".format(i))
            self.client.put_pixels(self.white)
            time.sleep(0.05)
            self.client.put_pixels(self.black)
            time.sleep(0.05)

    def test_fillsolid(self):
        for i in range(0, 50):
            self.fill_solid(10, 15, (255, 0, 0))
            time.sleep(.1)
            self.fill_solid(10, 15, (0, 0, 0))
            time.sleep(.1)
        self.client.put_pixels(self.black)

    def rainbow_cylon(self):
        for h in range(0, 255):

            # First slide the led in one direction
            for i in range(0, self.numleds):
                print("i is {} h is {}".format(i, h))
                self.fill_solid(i, 10, hsv_to_rgb(h, 1.0, 1.0))
            # time.sleep(.01)
            for i in range(self.numleds, 0):
                print("i is {} h is {}".format(i, h))
                self.fill_solid(i, 10, hsv_to_rgb(h, 1.0, 1.0))
                h = h - 1
        # time.sleep(.01)

        self.fill_solid(0, self.numleds, (0, 0, 0))
        self.client.put_pixels(self.black)

    def all(self, color):
        color_list = [color] * self.numleds
        self.client.put_pixels(color_list)

    def sunrise(self):
        transition_time = 1
        self.client.put_pixels(self.black)
        # fade from black to red
        for v in range(0, 255):
            hsv = (0, 1.0, v / 1.0 / 255)
            rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
            print("v is {}, hsv is {}, rgb is {} ".format(v, hsv, rgb))
            self.fill_solid(0, self.numleds, rgb)
            time.sleep(transition_time)
        # fade from red to orange
        v = 1
        for h in range(0, 60):
            hsv = (h, 1.0, v / 1.0 / 255)
            rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
            print("v is {}, hsv is {}, rgb is {} ".format(v, hsv, rgb))
            self.fill_solid(0, self.numleds, rgb)
            time.sleep(transition_time)
        self.client.put_pixels(self.white)
        time.sleep(transition_time * 2)
        self.client.put_pixels(self.black)

    def lightning(self):
        self.client.put_pixels(self.black)
        ledstart = random.randint(0, self.numleds)  # Determine starting location of flash
        ledlen = random.randint(0,
                                self.numleds - ledstart)  # // Determine length of flash (not to go beyond NUM_LEDS-1)
        flashes = random.randint(3, self.flashLimit)
        for flash_counter in range(0, flashes):
            print("flashcounter {} of flashes {}".format(flash_counter, flashes))
            if flash_counter == 0:
                dimmer = 5  # the brightness of the leader is scaled down by a factor of 5
            else:
                dimmer = random.randint(1, 3)  # return strokes are brighter than the leader
            color = hsv_to_rgb(60, .1, 1 / dimmer)
            self.fill_solid(ledstart, ledlen, color)

            self.random_delay(3, 16)

            if flash_counter == 0:
                time.sleep(.150)

            self.random_delay(0, 100, 50)

        self.client.put_pixels(self.black)
        self.random_delay(0, self.flashFrequency)

    def lightning_rainbow(self):
        self.client.put_pixels(self.black)
        ledstart = random.randint(0, self.numleds)  # Determine starting location of flash
        ledlen = random.randint(0,
                                self.numleds - ledstart)  # // Determine length of flash (not to go beyond NUM_LEDS-1)
        flashes = random.randint(3, self.flashLimit)
        for flash_counter in range(0, flashes):
            print("flashcounter {} of flashes {}".format(flash_counter, flashes))
            if flash_counter == 0:
                dimmer = 5  # the brightness of the leader is scaled down by a factor of 5
            else:
                dimmer = random.randint(1, 3)  # return strokes are brighter than the leader

            color = hsv_to_rgb(random.randint(0, 255), 1, 1 / dimmer)
            self.fill_solid(ledstart, ledlen, color)
            self.random_delay(3, 16)
            if flash_counter == 0:
                time.sleep(.150)
            self.random_delay(0, 100, 50)

        self.client.put_pixels(self.black)
        self.random_delay(0, self.flashFrequency)

    def fill_solid(self, ledstart, ledlen, color):
        if debug:
            print("color is {}".format(color))
        # hex = (dec2hex(color[0]), dec2hex(color[1]), dec2hex(color[2]))
        # print("hex is {}".format(hex))
        first = [(0, 0, 0)] * ledstart
        middle = [color] * ledlen
        last = [(0, 0, 0)] * (self.numleds - ledstart - ledlen)
        strip = first + middle + last
        self.client.put_pixels(strip)

    def random_delay(self, min_delay, max_delay, base=0):
        waiting = (base + random.randint(min_delay, max_delay)) / self.timefactor
        if debug:
            print("Waiting {} seconds.".format(waiting))
        time.sleep(waiting)


def dec2hex(d):
    """return a two character hexadecimal string representation of integer d"""
    return "%02X" % d


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
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def main():
    cloud = Cloud()
    print("Debug is {}, running with a timefactor of {}.".format(cloud.debug, 1 / cloud.timefactor))
    cloud.sunrise()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
