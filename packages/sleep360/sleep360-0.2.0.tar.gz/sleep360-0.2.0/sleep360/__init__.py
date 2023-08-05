#!/usr/bin/env python3

import time
import datetime

from sleep360.__about__ import (
    __author__,
    __email__,
    __description__,
    __url__,
    __license__,
    __version__,
)
from sleep360.dbus_bluez import Adapter
from sleep360.errors import Sleep360Error


name = "sleep360"


class Bulb:
    """Class used to control a Holi SleepCompanion.

    Exceptions:
    Sleep360Error() -- raised when the Blootooth connection fails
    """

    _adapter = None

    @classmethod
    def init_adapter(self, adapter_pattern=None):
        self._adapter = Adapter.new(adapter_pattern)
        if not self._adapter.is_powered():
            raise Sleep360Error("Bluetooth adapter is powered off.")

    def __init__(self, address=None, name=None, adapter_pattern=None):
        """Create a new object representing your bulb.

        Note that this constructor must be called with at least one address or one name.

        Keyword arguments:
        address -- MAC address of your SleepCompanion
        name -- Name of your SleepCompanion ("Bulb" by default)
        adapter_pattern -- your Linux bluetooth adapter name (ex. "hci0")
        """
        if self._adapter == None:
            self.init_adapter()
        self._device = self._adapter.new_device(address, name)

    def connect(self):
        """Connects to the bulb (bluetooth LE)."""
        self._device.connect()
        while (self._device.get_prop("ServicesResolved") == 0):
            time.sleep(0.1)
        self._init_services()

    def _init_services(self):
        gatt_services = self._device.get_gatt_services()

        service_hardware = gatt_services["00ff5502-3c25-45cb-99dc-1754766b829a"]
        service_application = gatt_services["01ff5502-3c25-45cb-99dc-1754766b829a"]
        service_bootloader = gatt_services["02ff5502-3c25-45cb-99dc-1754766b829a"]

        gatt_chrc_hardware = service_hardware.get_gatt_characteristics()
        gatt_chrc_application = service_application.get_gatt_characteristics()
        gatt_chrc_bootloader = service_bootloader.get_gatt_characteristics()

        self._chrc_off =            gatt_chrc_hardware["044993e6-5eed-439a-9497-9e4086539756"]
        self._chrc_temp =           gatt_chrc_hardware["0b4993e6-5eed-439a-9497-9e4086539756"]

        self._chrc_desc_light =     gatt_chrc_application["f04993e6-5eed-439a-9497-9e4086539756"]
        self._chrc_segment_light =  gatt_chrc_application["f14993e6-5eed-439a-9497-9e4086539756"]

    def disconnect(self):
        self._device.disconnect()

    def set_color(self, red, green, blue, warm, cold):
        """Turn ON the light if not already ON and set the given color.

        Arguments:
        red, green, blue -- RGB values (0x00 to 0xff)
        warm -- adjust the warmth of the light (0x00 to 0xff)
        cold -- adjust the coldness of the light (0x00 to 0xff)
        """
        self._chrc_desc_light.iface().WriteValue([
            0x00, 0x00, 0x01, 0x00], {})
        self._chrc_segment_light.iface().WriteValue([
            0x00, 0x00, 0x00, 0x00, 0x00,
            red & 0xff, green & 0xff, blue & 0xff,
            warm & 0xff, cold & 0xff], {})

    def off(self):
        """Turn OFF the light."""
        self._chrc_off.iface().WriteValue([0x00], {})

    def get_temperatures(self):
        """Retrieve temperatures from the bulb and return them.

        Return:
        a dict where keys are datetime.datetime objects
                     values are temperatures (float) given in Celsius
        """
        temp_map = {}
        temp_bytes = self._chrc_temp.iface().ReadValue({})
        i = 0
        while (i + 6) < len(temp_bytes):
            timestamp = ((temp_bytes[i + 3] << 24) |
                         (temp_bytes[i + 2] << 16) |
                         (temp_bytes[i + 1] << 8) |
                         (temp_bytes[i]))
            temperature = ((temp_bytes[i + 5] << 8) |
                           temp_bytes[i + 4]) / 10.0
            if timestamp:
                timestamp -= time.localtime().tm_gmtoff
                temp_map[datetime.datetime.fromtimestamp(timestamp)] = temperature
            i += 6
        return temp_map
