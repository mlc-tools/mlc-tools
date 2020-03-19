# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *
from .BaseEnum import BaseEnum


class TestEnum(BaseEnum):
    value1 = "value1"
    value2 = "value2"
    __slots__ = []

    def __init__(self):
        BaseEnum.__init__(self)

    def __hash__(self):
        return id(self)
