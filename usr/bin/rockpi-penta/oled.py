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
except Exception:
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
    draw.text((32, 8), 'Good Bye ~', font=font['14'], fill=255)
    disp_show()
    time.sleep(2)
    disp_clear()


def turn_off():
    misc.conf['show'].value = 0
    disp_clear()


def put_disk_info():
    k, v = misc.get_disk_info()
    text1 = 'Disk: {} {}'.format(k[0], v[0])

    if len(k) == 5:
        text2 = '{} {}  {} {}'.format(k[1], v[1], k[2], v[2])
        text3 = '{} {}  {} {}'.format(k[3], v[3], k[4], v[4])
        page = [
            {'xy': (0, -2), 'text': text1, 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': text2, 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': text3, 'fill': 255, 'font': font['11']},
        ]
    elif len(k) == 4:
        text2 = '{} {}  {} {}'.format(k[1], v[1], k[2], v[2])
        text3 = '{} {}'.format(k[3], v[3])
        page = [
            {'xy': (0, -2), 'text': text1, 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': text2, 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': text3, 'fill': 255, 'font': font['11']},
        ]
    elif len(k) == 3:
        text2 = '{} {}  {} {}'.format(k[1], v[1], k[2], v[2])
        page = [
            {'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': text2, 'fill': 255, 'font': font['12']},
        ]
    elif len(k) == 2:
        text2 = '{} {}'.format(k[1], v[1])
        page = [
            {'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': text2, 'fill': 255, 'font': font['12']},
        ]
    else:
        page = [{'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['14']}]

    return page

def put_disk_temp_info(pages_len):
    page = {}
    k, v = misc.get_disk_temp_info()

    if len(k) == 0:
        return page

    text1 = 'Disks Temp:'

    if len(k) == 4:
        text2 = '{} {}  {} {}'.format(k[0], v[0], k[1], v[1])
        text3 = '{} {}  {} {}'.format(k[2], v[2], k[3], v[3])
        page[pages_len] = [
            {'xy': (0, -2), 'text': text1, 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': text2, 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': text3, 'fill': 255, 'font': font['11']},
        ]
    elif len(k) == 3:
        text2 = '{} {}  {} {}'.format(k[0], v[0], k[1], v[1])
        text3 = '{} {}'.format(k[2], v[2])
        page[pages_len] = [
            {'xy': (0, -2), 'text': text1, 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': text2, 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': text3, 'fill': 255, 'font': font['11']},
        ]
    elif len(k) == 2:
        text2 = '{} {}  {} {}'.format(k[0], v[0], k[1], v[1])
        page[pages_len] = [
            {'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': text2, 'fill': 255, 'font': font['12']},
        ]
    elif len(k) == 1:
        text2 = '{}'.format(k[0], v[0])
        page[pages_len] = [
            {'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': text2, 'fill': 255, 'font': font['12']},
        ]
    else:
        page[pages_len] = [{'xy': (0, 2), 'text': text1, 'fill': 255, 'font': font['14']}]

    return page

def put_disk_io_info(pages_len):
    pages = {}
    page_index = pages_len
    disks = misc.get_disk_list('io_usage_mnt_points')

    for disk_mount, disk_dev in disks:
        pages[page_index] = [
            {'xy': (0, -2), 'text': 'Disk (' + disk_mount + '):', 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': misc.get_disk_io_read_info(disk_dev), 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': misc.get_disk_io_write_info(disk_dev), 'fill': 255, 'font': font['11']}
        ]
        page_index = page_index + 1

    return pages

def put_interface_info(pages_len):
    pages = {}
    page_index = pages_len
    interfaces = misc.get_interface_list()

    for x in interfaces:
        pages[page_index] = [
            {'xy': (0, -2), 'text': 'Network (' + x + '):', 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': misc.get_interface_rx_info(x), 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': misc.get_interface_tx_info(x), 'fill': 255, 'font': font['11']}
        ]
        page_index = page_index + 1

    return pages


def gen_pages():
    pages = {
        0: [
            {'xy': (0, -2), 'text': misc.get_info('up'), 'fill': 255, 'font': font['11']},
            {'xy': (0, 10), 'text': misc.get_cpu_temp(), 'fill': 255, 'font': font['11']},
            {'xy': (0, 21), 'text': misc.get_info('ip'), 'fill': 255, 'font': font['11']},
        ],
        1: [
            {'xy': (0, 2), 'text': misc.get_info('cpu'), 'fill': 255, 'font': font['12']},
            {'xy': (0, 18), 'text': misc.get_info('mem'), 'fill': 255, 'font': font['12']},
        ],
        2: put_disk_info()
    }

    pages.update(put_disk_temp_info(len(pages)))
    pages.update(put_disk_io_info(len(pages)))
    pages.update(put_interface_info(len(pages)))

    return pages


def slider(lock):
    with lock:
        misc.conf['show'].value = 1
        for item in misc.slider_next(gen_pages()):
            draw.text(**item)
        disp_show()


def auto_slider(lock):
    while misc.conf['slider']['auto']:
        if misc.conf['show'].value == 1:
            slider(lock)
        else:
            disp_clear()
        misc.slider_sleep()
    if misc.conf['show'].value == 1:
        slider(lock)
    else:
        disp_clear()
