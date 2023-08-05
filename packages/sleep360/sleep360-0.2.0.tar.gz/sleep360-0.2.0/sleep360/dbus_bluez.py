import dbus


from sleep360.errors import Sleep360Error


SERVICE_NAME = "org.bluez"
ADAPTER_INTERFACE = SERVICE_NAME + ".Adapter1"
DEVICE_INTERFACE = SERVICE_NAME + ".Device1"
GATT_SERVICE_INTERFACE = SERVICE_NAME + ".GattService1"
GATT_CHARACTERISTIC_INTERFACE = SERVICE_NAME + ".GattCharacteristic1"
GATT_DESCRIPTOR_INTERFACE = SERVICE_NAME + ".GattDescriptor1"


class BluezError(Sleep360Error):

    def __init__(self, msg):
        super().__init__("dbus-bluez", msg)


def get_managed_objects():
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object(SERVICE_NAME, "/"),
                             "org.freedesktop.DBus.ObjectManager")
    return manager.GetManagedObjects()


class BluezNode:

    def __init__(self, object_path, interface):
        self._dbus = dbus.SystemBus()
        self._interface = interface
        self._obj = self._dbus.get_object(SERVICE_NAME, object_path)
        self._iface = dbus.Interface(
            self._obj,
            self._interface)
        self._props = dbus.Interface(
            self._dbus.get_object(SERVICE_NAME, self._obj.object_path),
            "org.freedesktop.DBus.Properties")

    def get_prop(self, prop_name):
        return self._props.Get(self._interface, prop_name)

    def set_prop(self, prop_name, prop_value):
        return self._props.Set(self._interface, prop_name, prop_value)

    def iface(self):
        return self._iface


class GattDescriptor(BluezNode):

    def __init__(self, object_path):
        super().__init__(object_path, GATT_DESCRIPTOR_INTERFACE)


class GattCharacteristic(BluezNode):

    def __init__(self, object_path):
        super().__init__(object_path, GATT_CHARACTERISTIC_INTERFACE)

    def get_gatt_descriptors(self):
        gatt_dict = {}
        objects = get_managed_objects()
        for path, ifaces in objects.items():
            gatt_item = ifaces.get(GATT_DESCRIPTOR_INTERFACE)
            if (gatt_item != None and
                path.startswith(self._obj.object_path)):
                mybluez_obj = GattDescriptor(path)
                gatt_dict[mybluez_obj.get_prop("UUID")] = mybluez_obj
        return gatt_dict


class GattService(BluezNode):

    def __init__(self, object_path):
        super().__init__(object_path, GATT_SERVICE_INTERFACE)

    def get_gatt_characteristics(self):
        gatt_dict = {}
        objects = get_managed_objects()
        for path, ifaces in objects.items():
            gatt_item = ifaces.get(GATT_CHARACTERISTIC_INTERFACE)
            if (gatt_item != None and
                path.startswith(self._obj.object_path)):
                mybluez_obj = GattCharacteristic(path)
                gatt_dict[mybluez_obj.get_prop("UUID")] = mybluez_obj
        return gatt_dict


class Device(BluezNode):

    def __init__(self, object_path):
        super().__init__(object_path, DEVICE_INTERFACE)

    def connect(self):
        self._iface.Connect()

    def disconnect(self):
        self._iface.Disconnect()

    def is_connected(self):
        return (self.get_prop("Connected") == 1)

    def get_gatt_services(self):
        gatt_dict = {}
        objects = get_managed_objects()
        for path, ifaces in objects.items():
            gatt_service = ifaces.get(GATT_SERVICE_INTERFACE)
            if (gatt_service != None and
                path.startswith(self._obj.object_path)):
                mybluez_obj = GattService(path)
                gatt_dict[mybluez_obj.get_prop("UUID")] = mybluez_obj
        return gatt_dict


class Adapter(BluezNode):

    @classmethod
    def new(self, adapter_pattern=None):
        objects = get_managed_objects()
        for path, ifaces in objects.items():
            adapter = ifaces.get(ADAPTER_INTERFACE)
            if (adapter != None and
                (adapter_pattern == None or
                 adapter_pattern == adapter["Address"] or
                 path.endswith(adapter_pattern))):
                return Adapter(path)
        if adapter_pattern is None:
            raise BluezError("Bluetooth adapter not found")
        else:
            raise BluezError("Bluetooth adapter %s not found" % adapter_pattern)

    def __init__(self, object_path):
        super().__init__(object_path, ADAPTER_INTERFACE)

    def is_powered(self):
        return (self.get_prop("Powered") == 1)

    def power_on(self):
        self.set_prop("Powered", True)

    def power_off(self):
        self.set_prop("Powered", False)

    def new_device(self, device_address=None, device_name=None):
        if (device_address == None and
            device_name == None):
            raise BluezError("new_device() must be called with at least a device address or name")
        objects = get_managed_objects()
        for path, ifaces in objects.items():
            device = ifaces.get(DEVICE_INTERFACE)
            if (device != None) and path.startswith(self._obj.object_path):
                if ((device_address != None) and
                    (device["Address"] != device_address)):
                    continue
                if ((device_name != None) and
                    (device["Name"] != device_name)):
                    continue
                return Device(path)
        if (device_address != None and
            device_name != None):
            raise BluezError("Device (%s, %s) not found" %
                             (device_address, device_name))
        elif device_address != None:
            raise BluezError("Device %s not found" % device_address)
        else:
            raise BluezError("Device %s not found" % device_name)
