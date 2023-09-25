#!/usr/bin/env python3
import sys
import shutil
import mraa  # pylint: disable=import-error
from configparser import ConfigParser
from collections import defaultdict, OrderedDict

lv2dc = OrderedDict({
    'lv7': 0,
    'lv6': 0.12,
    'lv5': 0.25,
    'lv4': 0.37,
    'lv3': 0.5,
    'lv2': 0.62,
    'lv1': 0.75,
    'lv0': 0.999
    })


def set_mode(pin, mode=1):
    try:
        pin = mraa.Gpio(pin)
        pin.dir(mraa.DIR_OUT)
        pin.write(mode)
    except Exception as ex:
        print("Failed to set mode on GPIO pin", pin, ex)


def read_conf():
    conf = defaultdict(dict)
    cfg = ConfigParser()
    cfg.read('/etc/rockpi-penta.conf')

    # fan
    try:
        # Reverse compatibility for old configs
        # If none of the new value are founf in the cfg
        if bool(set(['lv4', 'lv5', 'lv6', 'lv7']) & set(cfg['fan'].keys())) == False:
            conf['fan']['lv0'] = cfg.getfloat('fan','lv0')
            conf['fan']['lv1'] = cfg.getfloat('fan','lv0')
            conf['fan']['lv2'] = cfg.getfloat('fan','lv1')
            conf['fan']['lv3'] = cfg.getfloat('fan','lv1')
            conf['fan']['lv4'] = cfg.getfloat('fan','lv2')
            conf['fan']['lv5'] = cfg.getfloat('fan','lv2')
            conf['fan']['lv6'] = cfg.getfloat('fan','lv3')
            conf['fan']['lv7'] = cfg.getfloat('fan','lv3')
        else:
            conf['fan']['lv0'] = cfg.getfloat('fan','lv0')
            conf['fan']['lv1'] = cfg.getfloat('fan','lv1')
            conf['fan']['lv2'] = cfg.getfloat('fan','lv2')
            conf['fan']['lv3'] = cfg.getfloat('fan','lv3')
            conf['fan']['lv4'] = cfg.getfloat('fan','lv4')
            conf['fan']['lv5'] = cfg.getfloat('fan','lv5')
            conf['fan']['lv6'] = cfg.getfloat('fan','lv6')
            conf['fan']['lv7'] = cfg.getfloat('fan','lv7')
    except Exception:
        conf['fan']['lv0'] = 35
        conf['fan']['lv1'] = 37
        conf['fan']['lv2'] = 40
        conf['fan']['lv3'] = 42
        conf['fan']['lv4'] = 44
        conf['fan']['lv5'] = 46
        conf['fan']['lv6'] = 48
        conf['fan']['lv7'] = 50

    # other
    try:
        conf['oled']['rotate'] = cfg.getboolean('oled', 'rotate')
        conf['oled']['f-temp'] = cfg.getboolean('oled', 'f-temp')
    except Exception:
        conf['oled']['rotate'] = False
        conf['oled']['f-temp'] = False

    return conf

def fan_temp2dc(t):
    for lv, dc in lv2dc.items():
        if t >= conf['fan'][lv]:
            return dc
    return 0.999


def open_pwm_i2c():
    def replace(filename, raw_str, new_str):
        with open(filename, 'r') as f:
            content = f.read()

        if raw_str in content:
            shutil.move(filename, filename + '.bak')
            content = content.replace(raw_str, new_str)

            with open(filename, 'w') as f:
                f.write(content)

    replace('/boot/hw_intfc.conf', 'intfc:pwm0=off', 'intfc:pwm0=on')
    replace('/boot/hw_intfc.conf', 'intfc:pwm1=off', 'intfc:pwm1=on')
    replace('/boot/hw_intfc.conf', 'intfc:i2c7=off', 'intfc:i2c7=on')


conf = {}
conf.update(read_conf())


if __name__ == '__main__':
    if sys.argv[-1] == 'open_pwm_i2c':
        open_pwm_i2c()
