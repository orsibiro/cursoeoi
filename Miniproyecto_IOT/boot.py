# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
from credentials import SSID, PASS
import time


wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASS)

print("conectando....")
while not wifi.isconnected():
    time.sleep_ms(100)

print("conectado con la ip {}".format(wifi.ifconfig()[0]))