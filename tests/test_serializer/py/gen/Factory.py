# -*- coding: utf-8 -*-
from tests.test_serializer.py.gen.IntrusivePtr import make_intrusive


class Factory(object):

    @staticmethod
    def build(type):
        if type == "AllTypesChildren":
            from .AllTypesChildren import AllTypesChildren
            return make_intrusive(AllTypesChildren)
        if type == "AllTypes":
            from .AllTypes import AllTypes
            return make_intrusive(AllTypes)
        if type == "DataUnit":
            from .DataUnit import DataUnit
            return make_intrusive(DataUnit)
        if type == "VisualUnit":
            from .VisualUnit import VisualUnit
            return make_intrusive(VisualUnit)
        return None
