#!/usr/bin/python3
import time
import misc
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font = {
    '10': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 10),
    '11': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 11),
    '12': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 12),
    '14': ImageFont.truetype('fonts/DejaVuSansMono-Bold.ttf', 14),
}

misc.set_mode(23, 0)
time.sleep(0.2)
misc.set_mode(23, 1)


def disp_init():
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=7)
    [getattr(disp, x)() for x in ('begin', 'clear', 'display')]
    return disp


try:
    disp = disp_init()
except Exception as ex:
    misc.open_pwm_i2c()
    time.sleep(0.2)
    disp = disp_init()

image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)


def disp_show():
    im = image.rotate(180) if misc.conf['oled']['rotate'] else image
    disp.image(im)
    disp.display()
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)


def disp_clear():
    disp_show()
    disp_show()


def welcome():
    disp_clear()
    draw.text((0, 0), 'ROCK Pi SATA HAT', font=font['14'], fill=255)
    draw.text((32, 16), 'loading...', font=font['12'], fill=255)
    disp_show()


def goodbye():
    disp_clear()
    draw.text((32, 8), 'Good Bye ~', font=font['14'], fill=255)
    disp_show()
