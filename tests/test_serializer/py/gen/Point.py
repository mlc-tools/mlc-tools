# -*- coding: utf-8 -*-

class Point(object):
    TYPE = "Point"
    __slots__ = ["row", "col"]

    def __init__(self, row=0, col=0):
        self.row = 0
        self.col = 0
        self.row = row
        self.col = col

    def __hash__(self):
        return id(self)

    def __eq__(self, rhs):
        result = True
        result = result and self.row == rhs.row
        result = result and self.col == rhs.col
        return result
        pass

    def __ne__(self, rhs):
        return not (self == rhs)
        pass

    def get_type(self):
        return Point.TYPE
        pass

    def serialize_xml(self, serializer):
        serializer.serialize(self.row, "row")
        serializer.serialize(self.col, "col")
        pass

    def deserialize_xml(self, serializer):
        self.row = serializer.deserialize("row", int, 0)
        self.col = serializer.deserialize("col", int, 0)
        pass

    def serialize_json(self, serializer):
        serializer.serialize(self.row, "row")
        serializer.serialize(self.col, "col")
        pass

    def deserialize_json(self, serializer):
        self.row = serializer.deserialize("row", int, 0)
        self.col = serializer.deserialize("col", int, 0)
        pass
