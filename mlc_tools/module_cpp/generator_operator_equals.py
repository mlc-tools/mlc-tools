from ..base.generator_operator_equals import GeneratorOperatorEqualsBase
from ..core.class_ import Class
from ..core.function import Function
from ..core.object import Objects


class GeneratorOperatorEquals(GeneratorOperatorEqualsBase):

    def __init__(self):
        GeneratorOperatorEqualsBase.__init__(self)

    def get_equal_method_name(self):
        return 'operator =='

    def get_not_equal_method_name(self):
        return 'operator !='

    def get_compare_method_pattern(self, cls, member):
        body_line = 'result = result && this->{0} == rhs.{0};'
        body_line_ptr = \
            'result = result && ((this->{0} == rhs.{0}) || ' \
            '(this->{0} != nullptr && rhs.{0} != nullptr && *this->{0} == *rhs.{0}));'
        return body_line_ptr if member.is_pointer or member.is_link else body_line

    def get_not_equal_method_operation(self):
        return 'return !(*this == rhs);'

    def add_copy_constructor(self, cls: Class):
        copy_constructor = Function()
        copy_constructor.name = cls.name
        copy_constructor.return_type = Objects.VOID
        copy_constructor.args.append(['rhs', GeneratorOperatorEqualsBase.get_const_ref(cls)])
        # operator.operations.append(self.get_not_equal_method_operation())

        copy_constructor.operations.append(f'this->operator=(rhs);')
        cls.functions.append(copy_constructor)

    def add_move_constructor(self, cls):
        pass

    def add_copy_operator(self, cls):
        copy_operator = Function()
        copy_operator.name = 'operator ='
        copy_operator.return_type = GeneratorOperatorEqualsBase.get_const_ref(cls)
        copy_operator.args.append(['rhs', GeneratorOperatorEqualsBase.get_const_ref(cls)])

        if cls.superclasses and cls.superclasses[0] != 'SerializedObject':
            parent = f'this->{cls.superclasses[0]}::operator=(rhs);'
            copy_operator.operations.append(parent)

        for member in cls.members:
            if member.is_static:
                continue
            if self.model.side == 'server' and member.name == '_reference_counter':
                copy_operator.operations.append(f'this->{member.name}.store(rhs.{member.name}.load());')
            else:
                copy_operator.operations.append(f'this->{member.name} = rhs.{member.name};')
        copy_operator.operations.append('return *this;')
        cls.functions.append(copy_operator)
