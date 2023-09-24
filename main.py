#!/usr/bin/env python3
import sys
import fan
import misc
try:
    import oled
    top_board = 1
except Exception as ex:
    top_board = 0
    print("Oled screen not supported")

import multiprocessing as mp

q = mp.Queue()

action = {
    'none': lambda: 'nothing',
    'slider': lambda: oled.slider(),
    'displayoff': lambda: oled.turn_off(),
    'switch': lambda: misc.fan_switch(),
    'reboot': lambda: misc.check_call('reboot'),
    'poweroff': lambda: misc.check_call('poweroff'),
}


def receive_key(q):
    while True:
        func = misc.get_func(q.get())
        if func != 'none':
            print("Key pressed:", func)
        action[func]()


def main():
    print("Service turned:", sys.argv[-1])
    if sys.argv[-1] == 'on':
        if top_board:
            oled.welcome()
    elif sys.argv[-1] == 'off':
        if top_board:
            oled.goodbye()
        exit(0)


if __name__ == '__main__':
    main()

    if top_board:
        p0 = mp.Process(target=receive_key, args=(q,))
        p1 = mp.Process(target=misc.watch_key, args=(q,))
        p2 = mp.Process(target=fan.running)

        p0.start()
        p1.start()
        p2.start()

        if misc.conf['show'].value == 1:
            print("Init with a slide")
            oled.slider()
        else:
            print("Init with nothing displayed")

        p2.join()
    else:
        p2 = mp.Process(target=fan.running)
        p2.start()
        p2.join()
