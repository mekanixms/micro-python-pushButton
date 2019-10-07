# The MIT License (MIT)
# Copyright (c) 2019 Cezar Lucan
# https://opensource.org/licenses/MIT

# MicroPython code for pushButton software debouncing
# generic implementation
# only tested on ESP8266 Amica and Lolin NodeMCU
# MicroPython v1.11-8-g48dcbbe60 on 2019-05-29
#
# https://github.com/mekanixms/micro-python-pushButton.git

import time
from buttonDebouncer import pushButton


def cb1(pin, s):
    print("Success cb invoked", pin)


def cb2(pin, s):
    print("Success cb invoke", pin)


push_button_debouncing_delay = 50

btn = pushButton(14, cb1)
btn1 = pushButton(17, cb2)

while True:
    pass
