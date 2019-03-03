from ..core.function import Function
from ..core.object import Object, Objects


class GeneratorOperatorEqualsBase(object):

    def __init__(self):
        pass

    def generate(self, model):
        for cls in model.classes:
            if cls.type == 'enum':
                continue
            if cls.is_inline:
                continue
            if cls.name in ['DataStorage']:
                continue
            self.add_equal_method(cls)
            self.add_not_equal_method(cls)

    @staticmethod
    def get_const_ref(cls_):
        ref = Object()
        ref.type = cls_.name
        ref.is_const = True
        ref.is_ref = True
        return ref

    def add_equal_method(self, cls):
        operator = Function()
        operator.name = self.get_equal_method_name()
        operator.return_type = Objects.BOOL
        operator.args.append(['rhs', GeneratorOperatorEqualsBase.get_const_ref(cls)])
        operator.is_const = True
        operator.operations.append('bool result = true;')
        for member in cls.members:
            if member.is_static or member.is_const or member.type == 'Observable':
                continue
            pattern = self.get_compare_method_pattern(cls, member)
            operator.operations.append(pattern.format(member.name))
        operator.operations.append('return result;')
        cls.functions.append(operator)

    def add_not_equal_method(self, cls):
        operator = Function()
        operator.name = self.get_not_equal_method_name()
        operator.return_type = Objects.BOOL
        operator.args.append(['rhs', GeneratorOperatorEqualsBase.get_const_ref(cls)])
        operator.is_const = True
        operator.operations.append(self.get_not_equal_method_operation())
        cls.functions.append(operator)

    def get_equal_method_name(self):
        return ''

    def get_not_equal_method_name(self):
        return ''

    # pylint: disable=unused-argument
    def get_compare_method_pattern(self, cls, member):
        return 'result = result && this->{0} == rhs.{0};'

    def get_not_equal_method_operation(self):
        return ''
