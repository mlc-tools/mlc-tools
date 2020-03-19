# -*- coding: utf-8 -*-


class Factory(object):

    @staticmethod
    def build(type):
        if type == "AllTypesChildren":
            from .AllTypesChildren import AllTypesChildren
            return AllTypesChildren()
        if type == "AllTypes":
            from .AllTypes import AllTypes
            return AllTypes()
        if type == "DataUnit":
            from .DataUnit import DataUnit
            return DataUnit()
        if type == "VisualUnit":
            from .VisualUnit import VisualUnit
            return VisualUnit()
        return None
