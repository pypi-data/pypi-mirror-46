#!/usr/bin/env python3

# pysmarthab - control devices in a SmartHab-powered home
# Copyright (C) 2019  Baptiste Candellier

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import abc
import enum

from .network import Endpoint

class DeviceType(enum.IntEnum):
    """Defines supported types of devices in SmartHab."""
    LIGHT = 1
    SHUTTER = 3
    THERMOSTAT = 5
    SENSOR_TEMP = 6
    SENSOR_MOTION = 23
    SENSOR_LUMINANCE = 8
    SENSOR_RELHUMIDITY = 7
    ELECT_SWITCH = 22
    POWER_METER = 16
    SMOKE_DETECTOR = 10


class Device(abc.ABC):
    """A device with basic properties and an editable state."""

    def __init__(self, client, type_id, device_id, label, room_label):
        self._client = client
        self.type_id = type_id
        self.device_id = device_id
        self.label = label
        self.room_label = room_label

        self.cached_state = None

    @staticmethod
    def _sh_state_to_py_type(state):
        if isinstance(state, str):
            clean_state = state.upper()
        else:
            clean_state = state

        if clean_state in ('OFF', ''):
            return False
        if clean_state == 'ON':
            return True
        if clean_state in ('NULL', '--'):
            return None

        return int(clean_state)

    @staticmethod
    def _py_state_to_sh_type(state):
        if isinstance(state, bool):
            if state:
                return 'ON'
            return 'OFF'

        if state is None:
            return 'NULL'

        return str(state)

    def update(self):
        """Retrieves and stores the device's current state."""
        res = self._client.send_request(Endpoint.GET_OBJECT_STATE,
                                        {'objet': self.device_id})
        self.cached_state = Device._sh_state_to_py_type(res)

    @property
    def state(self):
        """The device's state. Can be an int, a string, or a boolean."""
        return self.cached_state

    @state.setter
    def state(self, state):
        """Updates the device's state."""
        params = {
            'objet': self.device_id,
            'etat': Device._py_state_to_sh_type(state)
        }

        r_state = self._client.send_request(Endpoint.SET_OBJECT_STATE,
                                            params, verb='POST')
        self.cached_state = Device._sh_state_to_py_type(r_state)


class BinaryDevice(Device, abc.ABC):
    """A device with an OFF and an ON state."""

    def turn_off(self):
        """Turns off the device."""
        self.state = False

    def turn_on(self):
        """Turns on the device."""
        self.state = True

    def toggle(self):
        """Toggles the device's state."""
        self.state = not self.state


class Shutter(Device):
    """A device representing rolling shutters, with a state ranging from 0 to 100."""

    def __init__(self, client, device_id, label, room_label):
        super().__init__(client, DeviceType.SHUTTER, device_id, label, room_label)

    def close(self):
        """Closes the shutters."""
        self.state = 0

    def open(self):
        """Opens the shutters."""
        self.state = 100


class Light(BinaryDevice):
    """Represents a lightbulb with a binary ON/OFF state."""

    def __init__(self, client, device_id, label, room_label):
        super().__init__(client, DeviceType.LIGHT, device_id, label, room_label)


class Thermostat(Device):
    """Represents a thermostat."""

    def __init__(self, client, device_id, label, room_label):
        super().__init__(client, DeviceType.THERMOSTAT, device_id, label, room_label)

        self.setpointM = None
        self.setpoint0 = None
        self.setpoint1 = None
        self.setpointA = None
        self.tempMin = None
        self.tempMax = None

    def get_current_set_temp(self):
        """Returns the current set temperature. Not implemented."""

    def get_current_ambient_temp(self):
        """Returns the current ambient temperature. Not implemented."""

    def update_settings(self):
        """Updates the thermostat's full state"""
        res = self._client.get_single_device(self.device_id)

        # Copy up to date values to this object
        self.setpointM = res.setpointM
        self.setpoint0 = res.setpoint0
        self.setpoint1 = res.setpoint1
        self.setpointA = res.setpointA
        self.tempMin = res.tempMin
        self.tempMax = res.tempMax
