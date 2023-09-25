#!/usr/bin/env python3
import sys
import fan
import time
try:
    import oled
    top_board = 1
except Exception as ex:
    top_board = 0

import multiprocessing as mp

q = mp.Queue()

def main():
    if sys.argv[-1] == 'on':
        if top_board:
            oled.welcome()
            time.sleep(5)
            oled.disp_clear()
    elif sys.argv[-1] == 'off':
        if top_board:
            oled.goodbye()
            time.sleep(5)
            oled.disp_clear()
        fan.turn_off()


if __name__ == '__main__':
    main()

    p = mp.Process(target=fan.running)
    p.start()
    p.join()
