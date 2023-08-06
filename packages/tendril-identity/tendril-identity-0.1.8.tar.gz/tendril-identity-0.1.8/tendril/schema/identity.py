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


from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile
from tendril.schema.base import NakedSchemaObject
from tendril.schema.helpers import SchemaSelectableObjectSet
from tendril.schema.helpers import MultilineString
from tendril.config import instance_path
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class IdentitySignatory(NakedSchemaObject):
    def elements(self):
        e = super(IdentitySignatory, self).elements()
        e.update({
            'name':        self._p(('name',),),
            'designation': self._p(('designation',),),
        })
        return e

    def __repr__(self):
        return "<IdentitySignatory {0}, {1}>" \
               "".format(self.name, self.designation)


class IdentityBankAccountInfo(NakedSchemaObject):
    def elements(self):
        e = super(IdentityBankAccountInfo, self).elements()
        e.update({
            'accno':          self._p(('accno',),),
            'bank_name':      self._p(('bank_name',),),
            'branch_address': self._p(('branch_address',), ),
            'branch_code'   : self._p(('branch_code',), ),
            'micr':           self._p(('micr',), ),
            'ifsc':           self._p(('ifsc',), ),
        })
        return e

    def __repr__(self):
        return "<IdentityBankAccountInfo {0} {1}>" \
               "".format(self.bank_name, self.accno)


class IdentitySignatories(SchemaSelectableObjectSet):
    _objtype = IdentitySignatory


class IdentityBankAccounts(SchemaSelectableObjectSet):
    _objtype = IdentityBankAccountInfo


class TendrilPersona(SchemaControlledYamlFile):
    supports_schema_name = 'TendrilPersona'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, *args, **kwargs):
        self._signatory = kwargs.get('signatory', None)
        self._bank_account = kwargs.get('bank_account', None)
        super(TendrilPersona, self).__init__(*args, **kwargs)

    def elements(self):
        e = super(TendrilPersona, self).elements()
        e.update({
            '_ident':        self._p(('identity', 'ident'), ),
            'name':          self._p(('identity', 'name'), ),
            '_name_full':    self._p(('identity', 'name_full'),     required=False),  # noqa
            '_name_short':   self._p(('identity', 'name_short'),    required=False),  # noqa
            'phone':         self._p(('identity', 'phone'),         required=False),  # noqa
            'email':         self._p(('identity', 'email'),         required=False),  # noqa
            'website':       self._p(('identity', 'website'),       required=False),  # noqa
            'address':       self._p(('identity', 'address'),       required=False, parser=MultilineString),  # noqa
            'address_line':  self._p(('identity', 'address_line'),  required=False),  # noqa
            'iec':           self._p(('identity', 'iec'),           required=False),  # noqa
            'pan':           self._p(('identity', 'pan'),           required=False),  # noqa
            'cin':           self._p(('identity', 'cin'),           required=False),  # noqa
            'gstin':         self._p(('identity', 'gstin'),         required=False),  # noqa
            'logo':          self._p(('identity', 'logo'),          required=False, parser=instance_path),  # noqa
            'black_logo':    self._p(('identity', 'black_logo'),    required=False, parser=instance_path),  # noqa
            'square_logo':   self._p(('identity', 'square_logo'),   required=False, parser=instance_path),  # noqa
            'signatories':   self._p(('identity', 'signatories'),   required=False, parser=IdentitySignatories),   # noqa
            'bank_accounts': self._p(('identity', 'bank_accounts'), required=False, parser=IdentityBankAccounts),  # noqa
        })
        return e

    def schema_policies(self):
        policies = super(TendrilPersona, self).schema_policies()
        policies.update({})
        return policies

    @property
    def ident(self):
        return self._ident

    @property
    def name_short(self):
        return self._name_short or self.name

    @property
    def name_full(self):
        return self._name_full or self.name

    @property
    def signatory(self):
        return self.signatories[self._signatory]

    @signatory.setter
    def signatory(self, value):
        if value not in self.signatories.keys():
            raise ValueError("Unrecognized Signatory : {0}".format(value))
        self._signatory = value

    @property
    def bank_account(self):
        return self.bank_accounts[self._bank_account]

    @bank_account.setter
    def bank_account(self, value):
        if value not in self.bank_accounts.keys():
            raise ValueError("Unrecognized Bank Account : {0}".format(value))
        self._bank_account = value

    def __repr__(self):
        return "<TendrilPersona {0} {1}>".format(self.ident, self.path)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('TendrilPersona', TendrilPersona,
                        doc="Schema for Tendril Persona Definition Files")
