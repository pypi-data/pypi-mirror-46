#!/usr/bin/env python3

import time

from sleep360.dbus_bluez import Adapter
from sleep360.errors import Sleep360Error


name = "sleep360"


class Bulb:

    _adapter = None

    @classmethod
    def init_adapter(self, adapter_pattern=None):
        self._adapter = Adapter.new(adapter_pattern)
        if not self._adapter.is_powered():
            raise Sleep360Error("Bluetooth adapter is powered off.")

    def __init__(self, address=None, name=None, adapter_pattern=None):
        if self._adapter == None:
            self.init_adapter()
        self._device = self._adapter.new_device(address, name)

    def connect(self):
        self._device.connect()
        while (self._device.get_prop("ServicesResolved") == 0):
            time.sleep(0.1)
        self.init_services()

    def init_services(self):
        gatt_services = self._device.get_gatt_services()

        service_hardware = gatt_services["00ff5502-3c25-45cb-99dc-1754766b829a"]
        service_application = gatt_services["01ff5502-3c25-45cb-99dc-1754766b829a"]
        service_bootloader = gatt_services["02ff5502-3c25-45cb-99dc-1754766b829a"]

        gatt_chrc_hardware = service_hardware.get_gatt_characteristics()
        gatt_chrc_application = service_application.get_gatt_characteristics()
        gatt_chrc_bootloader = service_bootloader.get_gatt_characteristics()

        self._chrc_off = gatt_chrc_hardware["044993e6-5eed-439a-9497-9e4086539756"]
        self._chrc_segment_light = gatt_chrc_application["f14993e6-5eed-439a-9497-9e4086539756"]

    def disconnect(self):
        self._device.disconnect()

    def set_color(self, red, green, blue, warm, cold):
        self._chrc_segment_light.iface().WriteValue([
            0x00, 0x00, 0x00, 0x00, 0x00,
            red & 0xff, green & 0xff, blue & 0xff,
            warm & 0xff, cold & 0xff], {})

    def off(self):
        self._chrc_off.iface().WriteValue([0x00], {})
