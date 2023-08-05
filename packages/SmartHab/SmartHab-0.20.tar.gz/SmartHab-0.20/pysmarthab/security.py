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

import hmac
import collections

class Security:
    """Security functions to handle SmartHab HMAC generation"""
    @staticmethod
    def hmac_list(key, parameters):
        """Signs a list of parameters and returns the HMAC as an hex string"""
        msg = Security.params_to_query_string(parameters)
        return hmac.new(key.encode(), msg.encode(), 'sha256').hexdigest()

    @staticmethod
    def sign_params(key, parameters):
        """Adds HMAC signature to parameter list"""
        parameters.update({'sha': Security.hmac_list(key, parameters)})
        return parameters

    @staticmethod
    def params_to_query_string(parameters):
        """Sorts a list of parameters and convert them into a query string, without
        urlencoding them
        """
        items = collections.OrderedDict(sorted(parameters.items()))
        joined_items = map(lambda key: "{key}={items}".format(
            key=str(key), items=str(items[key])), items)
        query_str = '&'.join(joined_items)
        return query_str
