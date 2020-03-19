# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import json
from .common import *


class BaseEnum(object):
    TYPE = "BaseEnum"
    __slots__ = []

    def __init__(self):
        pass

    def __hash__(self):
        return id(self)

    def __eq__(self, rhs):
        result = True
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return BaseEnum.TYPE
        pass
