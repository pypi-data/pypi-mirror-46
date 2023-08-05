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

import enum
import json
import logging

import requests

from .security import Security
from .state import State

class Endpoint(enum.Enum):
    """SmartHab API endpoints"""
    GET_TOKEN = 'getToken'
    GET_NOTIFICATIONS = 'getNotifications'
    GET_OBJECTS = 'getObjects'
    GET_WEATHER = 'getMTO'
    GET_SETTINGS = 'getReglages'
    GET_INFOS = 'getInfos'
    GET_DASHBOARD_MODE = 'getModeDashboard'
    GET_OBJECT_STATE = 'getStateObject'
    GET_POWER_CONSUMPTION = 'getConsoElec'
    GET_HEATING = 'getChauffage'
    GET_SCENARIOS = 'getScenarios'
    SET_OBJECT_STATE = 'setObject'


class Network:
    """Network functions for SmartHab, designed to be mocked for testing"""

    def __init__(self, base_url, security=Security()):
        self.state = State()
        self.base_url = base_url
        self._security = security

    def _default_key(self):
        return self.state.token + str(self.state.uid)

    def send_request(self, endpoint, params=None, key=None, verb='GET'):
        """Sends a request to the SmartHab API to the given endpoint,
        with the given parameters, key and HTTP verb.
        """
        if key is None:
            key = self._default_key()

        all_params = self._make_full_query_params(key, params)

        logging.debug("sending %s request to endpoint %s", verb, endpoint)

        res = requests.request(verb,
                               "{base}/{endpoint}/".format(
                                   base=self.base_url, endpoint=endpoint.value),
                               params=all_params, headers={'Accept': 'application/json'}, timeout=30)

        if res.status_code in range(200, 300):
            return Network._parse_response(res.text)

        logging.error(
            "error while sending request, status code was %s", str(res.status_code))
        return None

    @staticmethod
    def _parse_response(response):
        if response == '':
            return response

        # API sometimes outputs PHP errors... sigh.
        # Only keep last line since JSON is only on one line anyway to remove
        # all that other garbage
        clean_text_res = response.splitlines()[-1]

        try:
            json_res = json.loads(clean_text_res)

            if isinstance(json_res, dict) and not json_res['success']:
                logging.error(
                    "request failed, response body: %s", clean_text_res)
                raise RequestFailedException(json_res['code'])

            return json_res
        except ValueError:
            return clean_text_res

    def _make_full_query_params(self, key, params):
        default_params = {
            'login': self.state.email,
            'device': self.state.device
        }

        if params is None:
            params = {}

        # Append login and device to required parameters
        params.update(default_params)

        # Sign the query, adding the SHA back to the param list
        return self._security.sign_params(key, params)


class RequestFailedException(Exception):
    """Raised when the response to a request was negative."""
    ERROR_INVALID_TOKEN = 11

    def __init__(self, error_code):
        self.error_code = error_code


class LoginRequiredException(Exception):
    """Raised when the user wasn't successfully authenticated and login is required."""
