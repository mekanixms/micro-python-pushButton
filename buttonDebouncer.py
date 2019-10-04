# The MIT License (MIT)
# Copyright (c) 2019 Cezar Lucan
# https://opensource.org/licenses/MIT

# MicroPython code for pushButton software debouncing
# generic implementation
# only tested on ESP8266 Amica and Lolin NodeMCU
#
# https://github.com/mekanixms/micro-python-pushButton.git

from utime import ticks_ms

from machine import Pin, disable_irq, enable_irq
import micropython
micropython.alloc_emergency_exception_buf(100)

_esp8266_safe_pins_ = [4, 5, 12, 13, 14]

push_button_debouncing_delay = 50  # ms

pin_ticks = {}
pin_cbs = {}


def wait_pin_rise(pin):
    if str(pin) not in pin_ticks:
        # mp does not support instance / dinamic atributes yet
        # to set the pin in the Pin instance and
        # cannot get pin number from the Pin class but str(PinInstance)
        # outputs as Pin(number) so I use this workaround
        pin_ticks[str(pin)] = {"utime": 0, "val": 0}

    if pin_ticks[str(pin)]["utime"] == 0:
        pin_ticks[str(pin)] = {"utime": ticks_ms()}
        pin.irq(trigger=Pin.IRQ_FALLING, handler=wait_pin_fall)


def wait_pin_fall(pin):
    delay_i_ = ticks_ms() - pin_ticks[str(pin)]["utime"]
    if delay_i_ > push_button_debouncing_delay:
        # signal on the FALLING edge -resets rising callback and pin utime to 0
        pin.irq(trigger=Pin.IRQ_RISING, handler=wait_pin_rise)
        pin_ticks[str(pin)]["utime"] = 0
        # success and have callback set - call it
        if callable(pin_cbs[str(pin)]):
            cb = pin_cbs[str(pin)]
            cb(pin, True)


class pushButton:
    def __init__(self, no, cb=None):
        if no in _esp8266_safe_pins_:
            self.pin_number = no
            self.pin = Pin(no, Pin.IN)
            self.cb = cb

            if callable(self.cb):
                global pin_cbs
                pin_cbs[str(self.pin)] = cb
                self.enable_irq()
        else:
            wm1 = "Pin not in whitelist"
            wm2 = "change it in the main module if you know what you do"
            print(wm1, wm2)

    def enable_irq(self):
        # in case we need to set / re set the callback later we need to recall this method
        if callable(self.cb):
            self.pin.irq(trigger=Pin.IRQ_RISING, handler=wait_pin_rise)
        else:
            print("IRQ Callback not set")
