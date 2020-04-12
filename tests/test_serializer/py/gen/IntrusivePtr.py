# -*- coding: utf-8 -*-


class IntrusivePtr(object):

    def __init__(self, instance):
        object.__setattr__(self, 'instance', instance)

    def __setattr__(self, name, value):
        object.__setattr__(object.__getattribute__(self, 'instance'), name, value)

    def __getattribute__(self, name):
        return object.__getattribute__(self, 'instance').__getattribute__(name)

    def __eq__(self, rhs):
        if rhs is None:
            return
        self_instance = object.__getattribute__(self, 'instance')
        rhs_instance = object.__getattribute__(rhs, 'instance')
        return self_instance.__eq__(rhs_instance)

    def __hash__(self):
        return id(object.__getattribute__(self, 'instance'))


def make_intrusive(class_name, *args):
    return IntrusivePtr(class_name(*args))
