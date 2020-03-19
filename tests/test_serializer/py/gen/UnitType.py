# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *
from .BaseEnum import BaseEnum


class UnitType(BaseEnum):
    attack = "attack"
    defend = "defend"
    support = "support"
    __slots__ = []

    def __init__(self):
        BaseEnum.__init__(self)

    def __hash__(self):
        return id(self)
