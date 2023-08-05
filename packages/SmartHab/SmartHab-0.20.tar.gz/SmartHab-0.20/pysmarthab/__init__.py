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

"""SmartHab home automation Python module.

Allows users to control their SmartHab devices.
"""
import logging
import datetime

from .network import *
from .device import *
from .security import *
from .state import *

class SmartHab:
    """The SmartHab class allows you to interact with the SmartHab API,
    including logging in, getting a list of available devices, and managing
    their state.
    """

    # SmartHab root API URL
    DEFAULT_BASE_API_URL = 'https://api.smarthab.tech'

    def __init__(self, base_url=DEFAULT_BASE_API_URL, state=None, network=None):
        self._network = network

        if self._network is None:
            self._network = Network(base_url)

        if state is not None:
            self._network.state = state

        self._state = self._network.state

    def login(self, email, password):
        """Logs in and stores the returned token in internal state."""
        self._state.token = None
        self._state.email = email
        self._state.password = password

        params = {
            'cle': str(password),
            'uid': str(self._state.uid)
        }

        try:
            res = self.send_request(
                Endpoint.GET_TOKEN, params, str(password))
            self._state.token = res['token']
        except RequestFailedException:
            pass

    def is_logged_in(self):
        """Checks if the user was logged in successfully."""
        return self._state.token is not None

    def get_device_list(self):
        """Gets a list of all available devices."""
        if not self.is_logged_in():
            raise LoginRequiredException

        res = self.send_request(Endpoint.GET_OBJECTS)

        # Cleanup response by flattening all devices to the list's top level
        flat_devices = []
        SmartHab._flatten_devices_list(flat_devices, res['objects'])

        # Map each JSON device to a well-known device object
        parsed = list(map(self._device_factory, flat_devices))
        logging.debug("found a total of %s devices", len(parsed))

        # Cleanup unknown or unwanted device types that couldn't be parsed
        devices = list(filter(lambda x: x is not None, parsed))
        logging.debug("found %s supported devices", len(devices))

        return devices

    def get_single_device(self, device_id):
        """Gets a single device from the complete device list, or None if not found."""
        device_list = self.get_device_list()
        device = next(
            (x for x in device_list if x.device_id == device_id), None)

        return device

    def send_request(self, endpoint, params=None, key=None, verb='GET'):
        try:
            return self._network.send_request(endpoint, params, key, verb)
        except RequestFailedException as ex:
            # Check if we need to renew the token
            if ex.error_code == RequestFailedException.ERROR_INVALID_TOKEN:
                logging.debug("renewing token...")
                self.login(self._state.email, self._state.password)

                # Retry, if re-login was successful
                if self.is_logged_in():
                    return self._network.send_request(endpoint, params, key, verb)
                else:
                    logging.error(
                        "token has invalidated and renewal attempt failed")
                    raise ex

            raise ex

    def _device_factory(self, device):
        family = int(device['id_famille'])

        if family == DeviceType.LIGHT:
            return Light(self, device['code'], device['objLabel'], device['pieceLabel'])

        if family == DeviceType.SHUTTER:
            return Shutter(self, device['code'], device['objLabel'], device['pieceLabel'])

        if family == DeviceType.THERMOSTAT:
            therm = Thermostat(
                self, device['code'], device['objLabel'], device['pieceLabel'])

            params = device['params']

            therm.setpointM = float(params['setpointM'])
            therm.setpoint0 = float(params['setpoint0'])
            therm.setpoint1 = float(params['setpoint1'])
            therm.setpointA = float(params['setpointA'])
            therm.tempMin = float(params['tempMin'])
            therm.tempMax = float(params['tempMax'])

            return therm

        return None

    @staticmethod
    def _flatten_devices_list(result, devices):
        """Take a list of devices all nested under different dicts associated
        to differents ids and flatten it into a simple list"""

        if 'params' in devices.keys():
            result.append(devices)
        else:
            for child in devices.values():
                if isinstance(child, list):
                    # Value is an array instead of a single object
                    for grandchild in child:
                        SmartHab._flatten_devices_list(result, grandchild)
                else:
                    SmartHab._flatten_devices_list(result, child)
