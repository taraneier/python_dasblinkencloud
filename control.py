import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import time
from cloud import Cloud
from radio import Radio
import sys


cloud = Cloud()
radio = Radio()

programs = cloud.get_programs()
program_index = 0

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()
draw.text((0, 0), "Initializing...", font=font, fill="white")
disp.image(image)
disp.show()
time.sleep(.2)


def shutdown():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), "shutdown started", font=font, fill="white")
    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.1)
    os.system("sudo shutdown -h now")

#
# def select_program(index):
#     print("program_index is {}".format(index))
#     global program_index
#     if index < 0:
#         index = len(programs) - 1
#     if index > len(programs) - 1:
#         index = 0
#     program_index = index
#
#     print("Index is {}, program is {}".format(program_index, programs[program_index]))
#
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0, 0, width, height), outline=0, fill=0)
#
#     draw.text((0, 0), "Loading %s" % programs[index], font=font, fill="white")
#
#     draw.text((0, 26), "Ready", font=font, fill="white")
#     # Display image.
#     disp.image(image)
#     disp.show()
#     time.sleep(.1)

def update_display():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), "{}".format(cloud), font=font, fill="white")
    draw.text((0,10), "{}".format(radio), font=font, fill="white")
    disp.image(image)
    disp.show()
    time.sleep(.1)


def run_program():
    cloud.run()
    # update_display()
    # try:
    #     func = getattr(cloud, programs[program_index])
    #     func()
    #     time.sleep(2)
    #
    # except AttributeError:
    #     print("function {} not found".format(programs[program_index]))
    # cloud.off()
    update_display()

def main():
    # select_program(0)
    # run_program()
    while True:
        if button_U.value:  # button is released
            pass
        else:  # button is pressed:
            radio.next()
            update_display()
            pass
        if button_L.value:  # button is released
            pass
        else:  # button is pressed:
            cloud.previous()
            update_display()
            continue
        if button_R.value:  # button is released
            pass
        else:  # button is pressed:
            cloud.next()
            update_display()
            continue
        if button_D.value:  # button is released
            pass
        else:  # button is pressed:
            radio.previous()
            update_display()
            pass

        if button_C.value:  # button is released
            pass
        else:  # button is pressed:
            pass

        if button_A.value:  # button is released

            pass
        else:  # button is pressed:
            radio.toggle()
            update_display()
            pass

        if button_B.value:  # button is released
            pass

        else:  # button is pressed:
            run_program()
            pass

        if not button_A.value and not button_B.value and not button_C.value:
            shutdown()
        else:
            # Display image.
            # disp.image(image)
            pass

        disp.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        cloud.off()
        radio.off()
        sys.exit(0)