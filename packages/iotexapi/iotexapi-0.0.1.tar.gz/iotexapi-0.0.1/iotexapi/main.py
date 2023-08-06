# -*- coding: utf-8 -*-

"""
    iotexapi.main
    ===============
"""

from eth_account.datastructures import AttributeDict
from urllib.parse import urlencode
from eth_utils import (
    apply_to_return_value,
    to_hex,
)
from hexbytes import HexBytes

from iotexapi import constants
from iotexapi.iotx import Iotx

from iotexapi.common.account import Address, PrivateKey, Account

class Iotex:

    _private_key = None
    _default_address = AttributeDict({})

    def __init__(self, **kwargs):
        """Connect to IoTeX blockchain.

        Args:
            kwargs (Any): We fill the most necessary parameters
            for working with blockchain
        """
        # We check the obtained nodes, if the necessary parameters
        # are not specified, then we take the default
        kwargs.setdefault('api', constants.DEFAULT_NODES['api'])

        self.iotx = Iotx(self, dict(api=kwargs.get('api')))

        # If the parameter of the private key is not empty,
        # then write to the variable
        if 'private_key' in kwargs:
            self.private_key = kwargs.get('private_key')
            self.default_address = Address.from_private_key(self.private_key) 

        # We check whether the default wallet address is set when
        # defining the class, and then written to the variable
        if 'default_address' in kwargs:
            self.default_address = kwargs.get('default_address')


    @property
    def private_key(self):
        """Get a private key"""
        return self._private_key

    @property
    def public_key(self):
        """Get public key"""
        private_key = PrivateKey(self._private_key)
        return private_key.public_key

    @private_key.setter
    def private_key(self, value: str) -> None:
        """Set a private key

        Args:
            value (str): Private key
        """
        try:
            private_key = PrivateKey(value)
        except ValueError:
            raise 'Invalid private key provided'

        self._private_key = str(private_key).lower()
        self.default_address = Address.from_private_key(self.private_key) 

    @property
    def default_address(self) -> AttributeDict:
        """Get a Address"""
        return self._default_address

    @default_address.setter
    def default_address(self, address: str) -> None:
        """Sets the address 
        Args:
             address (str) Address

        """
        self._default_address = address

    @property
    def address(self) -> Address:
        """Helper object that allows you to convert
        """
        return Address()

    @property
    def create_account(self) -> PrivateKey:
        """Create account

        Warning: Please control risks when using this API.
        To ensure environmental security, please do not invoke APIs
        provided by other or invoke this very API on a public network.

        """
        return Account.create()

   
   