#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import glob

from tendril import schema
from tendril.config import PRIMARY_PERSONA

from tendril.config import instance_path
from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


class IdentityManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._identities_loaded = {}
        self._load_identities()

    @property
    def primary_persona(self):
        return self._identities_loaded[PRIMARY_PERSONA]

    def _load_identities(self):
        candidates = glob.glob(
            os.path.join(instance_path('identity'), '*.yaml')
        )
        for candidate in candidates:
            persona = schema.load(candidate)
            self._identities_loaded[persona.ident] = persona

    def __getattr__(self, item):
        return self._identities_loaded[item]
