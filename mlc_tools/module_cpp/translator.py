from ..base.translator_base import TranslatorBase
from ..core.object import Objects, Object, AccessSpecifier
from ..core.function import Function
from .regex import RegexPatternCpp


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def translate_function(self, cls, method, model):
        if not method.translated:
            body = '\n'.join(method.operations)
            body = self.translate_function_body(body)
            method.body = body
        else:
            if method.operations:
                method.body = '\n'.join(method.operations)
            else:
                method.body = ''

    def translate_function_body(self, func):
        if not func:
            func = ''
        func = self.replace_by_regex(func)
        # func = Translator.convert_braces_to_tabs(func)
        # func = Translator.remove_double_eol(func)
        # func = Translator.add_imports(cls, func, model)
        return func

    def convert_to_enum(self, cls):
        cast = 'int'
        values = []

        def get_enum_value(cls_, index):
            return '(1 << {})'.format(index) if not cls_.is_numeric else str(index)

        def translate_members():
            shift = 0
            for member in cls.members:
                if member.name:
                    continue
                member.name = member.type
                member.type = cast
                member.is_static = True
                member.is_const = True
                if member.initial_value is None:
                    member.initial_value = get_enum_value(cls, shift)
                values.append(1 << shift)
                shift += 1

        def add_method(type_, name, const):
            method = Function()
            method.return_type = type_
            method.name = name
            method.is_const = const
            cls.functions.append(method)
            return method

        def create_const_ref():
            const_ref = Object()
            const_ref.type = cls.name
            const_ref.is_const = True
            const_ref.is_ref = True
            return const_ref

        def add_constructor_with_parameter():
            method = add_method(Object(), cls.name, False)
            method.args.append(['_value', Objects.INT])
            method.operations.append('value = _value;')

        def add_constructor_copy():
            method = add_method(Object(), cls.name, False)
            method.args.append(['rhs', create_const_ref()])
            method.operations.append('value = rhs.value;')

        def add_constructor_with_string():
            method = add_method(Object(), cls.name, False)
            method.args.append(['_value', Objects.STRING])
            for index, obj in enumerate(cls.members):
                if obj.name != 'value' and index <= len(values):
                    method.operations.append('''if(_value == "{0}")
                    {{
                        value = {0};
                        return;
                    }}'''.format(obj.name))
            method.operations.append('value = 0;')

        def add_operator_copy():
            method = add_method(create_const_ref(), 'operator =', False)
            method.args.append(['rhs', create_const_ref()])
            method.operations.extend(['value = rhs.value;', 'return *this;'])

        def add_operator_copy_with_int():
            method = add_method(create_const_ref(), 'operator =', False)
            method.args.append(['rhs', Objects.INT])
            method.operations.extend(['value = rhs;', 'return *this;'])

        def add_operator_copy_with_string():
            method = add_method(create_const_ref(), 'operator =', False)
            method.args.append(['_value', Objects.STRING])
            for index, obj in enumerate(cls.members):
                if obj.name != 'value' and index <= len(values):
                    method.operations.append('''if(_value == "{0}")
                                {{
                                    value = {0};
                                    return *this;
                                }}'''.format(obj.name))
            method.operations.append('return *this;')

        def add_operator_equals():
            method = add_method(Objects.BOOL, 'operator ==', True)
            method.args.append(['rhs', create_const_ref()])
            method.operations.append('return value == rhs.value;')

        def add_operator_equals_with_int():
            method = add_method(Objects.BOOL, 'operator ==', True)
            method.args.append(['rhs', Objects.INT])
            method.operations.append('return value == rhs;')

        def add_operator_less():
            method = add_method(Objects.BOOL, 'operator <', True)
            method.args.append(['rhs', create_const_ref()])
            method.operations.append('return value < rhs.value;')

        def add_cast_to_int():
            method = add_method(Object(), 'operator int', True)
            method.operations.append('return value;')

        def add_operator_cast_string():
            method = add_method(Object(), 'operator std::string', True)
            for index, obj in enumerate(cls.members):
                if obj.name != 'value' and index <= len(values):
                    method.operations.append('''if(value == {0})
                    {{
                        return "{0}";
                    }}'''.format(obj.name))
            method.operations.append('return std::string();')

        def add_method_str():
            method = add_method(Objects.STRING, 'str', True)
            for index, obj in enumerate(cls.members):
                if obj.name != 'value' and index <= len(values):
                    method.operations.append('''if(value == {0})
                                {{
                                    return "{0}";
                                }}'''.format(obj.name))
            method.operations.append('return std::string();')

        def add_member_value():
            value = Object()
            value.initial_value = cls.members[0].name
            value.name = 'value'
            value.type = cast
            value.access = AccessSpecifier.private
            cls.members.append(value)

        translate_members()
        add_constructor_with_parameter()
        add_constructor_copy()
        add_constructor_with_string()
        add_operator_copy()
        add_operator_copy_with_int()
        add_operator_copy_with_string()
        add_operator_equals()
        add_operator_equals_with_int()
        add_operator_less()
        add_cast_to_int()
        add_operator_cast_string()
        add_method_str()
        add_member_value()

        return values

    def replace_by_regex(self, body):
        for reg in RegexPatternCpp.FUNCTION:
            body = self.replace(body, reg)
        for reg in RegexPatternCpp.REPLACES:
            body = body.replace(reg[0], reg[1])
        for reg in RegexPatternCpp.convert_c17_to_c14:
            body = self.replace(body, reg)
        return body
