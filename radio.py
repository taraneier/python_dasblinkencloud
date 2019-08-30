import sys
from omxplayer.player import OMXPlayer

class Radio:
    def __init__(self):
        self.stations = [('KPOA', 'https://16693.live.streamtheworld.com/KPOAFM.mp3 '),
                         ('KAZU', 'https://icecastle.csumb.edu/live128'),
                         ('KZSC', 'http://streaming.kzsc.org:8000/kzschigh')
                         ]
        self.station_index = 0
        self.play = False
        self.player = False

    def __str__(self):
        state = ""
        if self.play:
            state = "on"
        else:
            state = "off"
        return "{} -- {}".format(self.stations[self.station_index][0], state)

    def get_stations(self):
        return self.stations

    def current(self):
        return self.stations[self.station_index]

    def next(self):
        if self.play:
            self.off()
        self.station_index = self.station_index + 1
        if self.station_index > len(self.stations) - 1:
            self.station_index = 0
        return self.stations[self.station_index]

    def previous(self):
        if self.play:
            self.off()
        self.station_index = self.station_index - 1
        if self.station_index < 0:
            self.station_index = len(self.stations) - 1
        return self.stations[self.station_index]

    def toggle(self):
        self.play = not self.play
        if not self.play:
            self.off()
        else:
            self.on()
        return self.play

    def on(self):
        self.play = True
        print("playing {}".format(self.stations[self.station_index][0]))
        self.player = OMXPlayer(self.stations[self.station_index][1])
        return self.play

    def off(self):
        self.play = False
        if self.player:
            print("stopping {}".format(self.stations[self.station_index][0]))
            self.player.quit()
        return self.play


def main():
    print("in radio main, wtf")
    radio = Radio()
    print(radio.on())
    print(radio.next())
    print(radio.toggle())
    print(radio.next())
    print(radio.previous())
    print(radio.toggle())
    print(radio.next())
    print(radio.next())
    print(radio.next())
    print(radio.next())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

