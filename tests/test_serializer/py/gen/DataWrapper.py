# -*- coding: utf-8 -*-


class DataWrapper(object):

    def __init__(self, instance):
        object.__setattr__(self, 'instance', instance)

    def __setattr__(self, name, value):
        object.__setattr__(object.__getattribute__(self, 'instance'), name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, 'instance').__getattribute__(name)
