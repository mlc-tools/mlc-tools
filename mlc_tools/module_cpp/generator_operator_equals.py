from ..core.object import *
from ..core.function import Function


class GeneratorOperatorEquals(object):

    def __init__(self):
        pass

    def generate(self, model):
        for cls in model.classes:
            if cls.type == 'enum':
                continue
            if cls.name in ['DataStorage']:
                continue
            self.add_operators_equals(cls)

    @staticmethod
    def add_operators_equals(cls):
        def get_const_ref():
            ref = Object()
            ref.type = cls.name
            ref.is_const = True
            ref.is_ref = True
            return ref

        operator = Function()
        operator.name = 'operator =='
        operator.return_type = Objects.BOOL
        operator.args.append(['rhs', get_const_ref()])
        operator.is_const = True
        operator.operations.append('bool result = true;')
        body_line = 'result = result && {0} == rhs.{0};'
        for m in cls.members:
            if m.is_static or m.is_const or m.type == 'Observable':
                continue
            operator.operations.append(body_line.format(m.name))
        operator.operations.append('return result;')
        cls.functions.append(operator)

        operator = Function()
        operator.name = 'operator !='
        operator.return_type = Objects.BOOL
        operator.args.append(['rhs', get_const_ref()])
        operator.is_const = True
        operator.operations.append('bool result = false;')
        body_line = 'result = result || {0} != rhs.{0};'
        for m in cls.members:
            if m.is_static or m.is_const or m.type == 'Observable':
                continue
            operator.operations.append(body_line.format(m.name))
        operator.operations.append('return result;')
        cls.functions.append(operator)
