from ..base.generator_operator_equals import GeneratorOperatorEqualsBase


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
