# Sleep360

This project allows to control the Holi SleepCompanion from a Linux computer.

The SleepCompanion is nice LED bulb that offers a lot of features to improve your sleep and your waking up.
It is manufactured by Holi, a French company.
A product description can be found by following these links:

- [Official Website (French)](https://www.holi.io/?portfolio=sleepcompanion-lampoule-qui-vous-reveille-les-neurones)
- [An English overview](https://www.hobbr.com/holi-sleep-companion)

This Sleep360 project is written in Python and can be used:

- as a library by creating a `sleep360.Bulb()` object
- as a command line utility (coming soon)

## Requirements

- D-BUS
- bluez >= 5.46 (dependency on the GATT D-BUS API)

## Installation

Coming soon...

## Command line usage

Coming soon...

## Library usage

Coming soon...

## Supported features

The SleepCompanion bulb offers a lot of features.
Among them, the following ones are currently supported by Sleep360:

- Setting colors (RGB + warm and cold value)
- Powering off the bulb

## Reverse-engineering

This project has been developed by carefully studying the Bluetooth LE messages.
The file [BLE-protocol.md](BLE-protocol.md) describes my understanding of these messages.
