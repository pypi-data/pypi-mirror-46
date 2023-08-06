#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ontology.smart_contract.native_contract.asset import Asset
from ontology.smart_contract.native_contract.ontid import OntId
from ontology.smart_contract.native_contract.governance import Governance


class NativeVm(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    def asset(self):
        return Asset(self.__sdk)

    def ont_id(self):
        return OntId(self.__sdk)

    def governance(self):
        return Governance(self.__sdk)
