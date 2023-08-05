#!/usr/bin/env python3

import sys
import time

from sleep360 import Bulb


def main():
    bulb = Bulb(name="Bulb")

    bulb.connect()
    bulb.set_color(0xff, 0x00, 0x00, 0x00, 0x00)
    time.sleep(2)
    bulb.off()
    bulb.disconnect()
    return 0


if __name__ == '__main__':
    sys.exit(main())
