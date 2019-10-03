# The MIT License (MIT)
# Copyright (c) 2019 Cezar Lucan
# https://opensource.org/licenses/MIT

# MicroPython code for pushButton software debouncing
# generic implementation
# only tested on ESP8266 Amica and Lolin NodeMCU

# Documentation:
#   https://github.com/mekanixms
#
# Example file for pushButton software debouncer
import time
from buttonDebouncer import pushButton


def cb14(pin, s):
    print("Success cb invoke", pin)


push_button_debouncing_delay = 50

btn = pushButton(14, cb14)
btn1 = pushButton(17, cb14)

while True:
    pass
