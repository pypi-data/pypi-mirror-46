# Copyright 2019 Robert Ginda <rginda@gmail.com>
# This code is licensed under MIT license (see LICENSE.md for details)
#

"""
Python library to interface with Robotronic/Easylap USB compatible r/c car lap
counters.
"""

from cp2110 import *

EASYLAP_PID = 0x86B9

if __name__ == '__main__':
  import time
  d = CP2110Device(pid=EASYLAP_PID)
  d.set_uart_config(UARTConfig(
    baud=38400, parity=PARITY.NONE, flow_control=FLOW_CONTROL.DISABLED,
    data_bits=DATA_BITS.EIGHT, stop_bits=STOP_BITS.SHORT))
  d.enable_uart()

  buf = []

  while True:
    chunk = d.read(RX_TX_MAX + 1)
    while chunk:
      buf += chunk
      chunk = d.read(RX_TX_MAX + 1)

    #if buf:
    #  print(['%.2X' % int(x) for x in buf])

    while len(buf) >= 3:
      if buf[0] == 0x0B and buf[2] == 0x83:
        # timer packet
        if len(buf) >= 0x0B:
          timer_value = (buf[3] | buf[4] << 8 | buf[5] << 16 | buf[6] << 32)
          print("timer: %s" % timer_value)
          buf = buf[0x0B + 1:]
          continue

      if buf[0] == 0x0D and buf[2] == 0x84:
        # car packet
        if len(buf) >= 0x0D:
          uid = (buf[3] | buf[4] << 8)
          timer_value = (buf[7] | buf[8] << 8 | buf[9] << 16 | buf[10] << 32)
          print("car: %s: %s" % (uid, timer_value))
          buf = buf[0x0D + 1:]
          continue

      buf = buf[1:]

    time.sleep(0.025)
