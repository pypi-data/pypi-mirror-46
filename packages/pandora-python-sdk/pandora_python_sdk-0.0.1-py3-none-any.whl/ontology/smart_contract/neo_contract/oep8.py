#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from ontology.common.address import Address
from ontology.account.account import Account
from ontology.exception.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.utils.contract_data import ContractDataParser
from ontology.utils.contract_event import ContractEventParser
from ontology.smart_contract.neo_contract.invoke_function import InvokeFunction


class Oep8(object):
    def __init__(self, sdk):
        self.__sdk = sdk
        self.__hex_contract_address = ''

    @property
    def hex_contract_address(self):
        return self.__hex_contract_address

    @hex_contract_address.setter
    def hex_contract_address(self, hex_contract_address: str):
        if not isinstance(hex_contract_address, str) and len(hex_contract_address) == 40:
            raise SDKException(ErrorCode.require_str_params)
        self.__hex_contract_address = hex_contract_address

    def __get_token_setting(self, func_name: str,token_id) -> str:
        func = InvokeFunction(func_name)
        func.set_params_value(token_id)
        res = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        return res.get('Result', '')

    @staticmethod
    def __b58_address_check(b58_address):
        if not isinstance(b58_address, str):
            raise SDKException(ErrorCode.param_err('the data type of base58 encode address should be the string.'))
        if len(b58_address) != 34:
            raise SDKException(ErrorCode.param_err('the length of base58 encode address should be 34 bytes.'))

    def get_name(self,token_id) -> str:
        """
        This interface is used to call the Name method in ope4
        that return the name of an oep4 token.

        :return: the string name of the oep4 token.
        """
        name = self.__get_token_setting('name',token_id)
        return ContractDataParser.to_utf8_str(name)

    def get_symbol(self,token_id) -> str:
        """
        This interface is used to call the Symbol method in ope4
        that return the symbol of an oep4 token.

        :return: a short string symbol of the oep4 token
        """
        symbol = self.__get_token_setting('symbol',token_id)
        return ContractDataParser.to_utf8_str(symbol)

    def get_decimal(self,token_id) -> int:
        """
        This interface is used to call the Decimal method in ope4
        that return the number of decimals used by the oep4 token.

        :return: the number of decimals used by the oep4 token.
        """
        decimals = self.__get_token_setting('decimals',token_id)
        return ContractDataParser.to_int(decimals)


    def get_total_supply(self,token_id) -> int:
        """
        This interface is used to call the TotalSupply method in ope4
        that return the total supply of the oep4 token.

        :return: the total supply of the oep4 token.
        """
        func = InvokeFunction('totalSupply')
        func.set_params_value(token_id)
        response = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        try:
            total_supply = ContractDataParser.to_int(response['Result'])
        except SDKException:
            total_supply = 0
        return total_supply

    def check_token_id(self,token_id) -> int:
        """

        """
        func = InvokeFunction('checkTokenId')
        func.set_params_value(token_id)
        response = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        print(response)
        try:
            exist = ContractDataParser.to_int(response['Result'])
        except SDKException:
            exist = "dd"
        return exist


    def total_balance_of(self, b58_address: str) -> int:
        """
        This interface is used to call the BalanceOf method in ope4
        that query the ope4 token balance of the given base58 encode address.

        :param b58_address: the base58 encode address.
        :return: the oep4 token balance of the base58 encode address.
        """
        func = InvokeFunction('totalBalanceOf')
        Oep8.__b58_address_check(b58_address)
        address = Address.b58decode(b58_address).to_bytes()
        func.set_params_value(address)
        result = self.__sdk.get_network().send_neo_vm_transaction_pre_exec(self.__hex_contract_address, None, func)
        try:
            balance = ContractDataParser.to_int(result['Result'])
        except SDKException:
            balance = 0
        return balance
