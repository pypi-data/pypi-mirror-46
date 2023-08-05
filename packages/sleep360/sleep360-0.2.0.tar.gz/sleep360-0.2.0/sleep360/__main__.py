#!/usr/bin/env python3

import cmd

import sleep360
from sleep360 import Bulb
from sleep360 import Sleep360Error

ERROR_NOT_CONNECTED = "ERROR: The SleepCompanion must be connected first"
ERROR_NB_ARGUMENTS = "ERROR: Wrong number of arguments"


class BulbShell(cmd.Cmd):

    intro = "\
Sleep360 shell (version %s).\n\
Type help or ? to list commands.\n" % sleep360.__version__
    prompt = "[sleep360] "

    def __init__(self):
        super().__init__()
        self._bulb = None

    def _help_cmd(self, usage, desc=None, args=None, ret=None):
        print("\
Usage:\n\
    %s\n" % usage)
        if desc:
            print("    %s\n" % desc)
        if args:
            print("Arguments:")
            for (a, desc) in args:
                print("    %s -- %s" % (a, desc));

    def help_exit(self):
        usage = "exit"
        desc = "Exit from Sleep360 shell."
        self._help_cmd(usage, desc=desc)

    def do_exit(self, arg):
        args = arg.split()
        if len(args) != 0:
            print(ERROR_NB_ARGUMENTS)
            return False
        if self._bulb:
            print("Disconnecting from the Bulb...")
            self._bulb.disconnect()
            self._bulb = None
        return True

    def do_EOF(self, arg):
        """Called when Ctrl-D is pressed"""
        return self.do_exit(arg)

    def help_connect(self):
        usage = "connect NAME [ADDRESS]"
        desc = "Connect to the SleepCompanion."
        args = [("NAME", "name of the bluetooth device (\"Bulb\" by default)"),
                ("ADDRESS", "MAC address of the device (optional)")]
        self._help_cmd(usage, desc=desc, args=args)

    def do_connect(self, arg):
        args = arg.split()
        if len(args) not in (1, 2):
            print(ERROR_NB_ARGUMENTS)
            return False
        if self._bulb:
            print("Warning: A bulb is already connected, nothing to do.")
            return False
        print("Connecting to the Bulb...")
        try:
            if len(args) == 2:
                self._bulb = Bulb(name=args[0], address=args[1])
            else:
                self._bulb = Bulb(name=args[0])
            self._bulb.connect()
        except Sleep360Error as e:
            print(e)
            self._bulb = None

    def help_disconnect(self):
        usage = "disconnect"
        desc = "Disconnect from the SleepCompanion."
        self._help_cmd(usage, desc=desc)

    def do_disconnect(self, arg):
        args = arg.split()
        if len(args) != 0:
            print(ERROR_NB_ARGUMENTS)
            return False
        if self._bulb == None:
            print("WARNING: Nothing to do");
            return False
        print("Disconnecting from the Bulb...")
        try:
            self._bulb.disconnect()
        finally:
            self._bulb = None

    def help_set_color(self):
        usage = "set_color RGB WARM COLD"
        desc = "\
Turn ON the light if not already ON and set the given color. \
Argument values must be given in hexadecimal."
        args = [("RGB", "RGB values (from 0x000000 to 0xffffff)"),
                ("WARM", "warmth of the light (0x00 to 0xff)"),
                ("COLD", "coldness of the light (0x00 to 0xff)")]
        self._help_cmd(usage, desc=desc, args=args)

    def do_set_color(self, arg):
        if self._bulb == None:
            print(ERROR_NOT_CONNECTED)
            return False
        args = arg.split()
        if len(args) != 3:
            print(ERROR_NB_ARGUMENTS)
            return False
        try:
            color = int(args[0], 16)
            w = int(args[1], 16)
            c = int(args[2], 16)
            self._bulb.set_color((color & 0xff0000) >> 16,
                                 (color & 0x00ff00) >> 8,
                                 (color & 0x0000ff),
                                 warm=w, cold=c)
        except ValueError as e:
            print(e)
        except Sleep360Error as e:
            print(e)

    def help_off(self):
        usage = "off"
        desc = "Turn OFF the light"
        self._help_cmd(usage, desc=desc)

    def do_off(self, arg):
        if self._bulb == None:
            print(ERROR_NOT_CONNECTED)
            return False
        args = arg.split()
        if len(args) != 0:
            print(ERROR_NB_ARGUMENTS)
            return False
        try:
            self._bulb.off()
        except Sleep360Error as e:
            print(e)

    def help_get_last_temperature(self):
        usage = "get_last_temperature"
        desc = "Retrieve temperatures and display the most recent one"
        self._help_cmd(usage, desc=desc)

    def do_get_last_temperature(self, arg):
        if self._bulb == None:
            print(ERROR_NOT_CONNECTED)
            return False
        args = arg.split()
        if len(args) != 0:
            print(ERROR_NB_ARGUMENTS)
            return False
        try:
            temperatures = self._bulb.get_temperatures()
            last_timestamp = max(temperatures.keys())
            print("At %s: %0.2f℃" % (last_timestamp, temperatures[last_timestamp]))
        except Sleep360Error as e:
            print(e)

    def help_get_all_temperatures(self):
        usage = "get_all_temperatures"
        desc = "Retrieve temperatures and display them"
        self._help_cmd(usage, desc=desc)

    def do_get_all_temperatures(self, arg):
        if self._bulb == None:
            print(ERROR_NOT_CONNECTED)
            return False
        args = arg.split()
        if len(args) != 0:
            print(ERROR_NB_ARGUMENTS)
            return False
        try:
            temperatures = self._bulb.get_temperatures()
            for (d, t) in temperatures.items():
                print("%s: %.2f℃" % (d, t))
        except Sleep360Error as e:
            print(e)


if __name__ == '__main__':
    BulbShell().cmdloop()
