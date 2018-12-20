import re
from .regex import RegexPatternPhp
from ..core.object import *
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def translate_function(self, cls, method, model):
        if not method.translated:
            body = '\n'.join(method.operations)
            body = self.translate_function_body(cls, body, model, method.args)
            method.body = body
        else:
            if len(method.operations) > 0:
                method.body = '\n        '.join(method.operations)

    @staticmethod
    def translate_function_body(cls, func, model, args):
        func = Translator.replace_by_regex(func, model, args)
        func = Translator.add_imports(cls, func, model)
        return func

    def convert_to_enum(self, cls):
        shift = 0
        cast = 'string'
        values = []
        for m in cls.members:
            if len(m.name):
                continue
            m.name = m.type
            m.type = cast
            m.is_static = True
            m.is_const = True
            if m.initial_value is None:
                if cast == 'int':
                    m.initial_value = '(1 << {})'.format(shift)
                    values.append(1 << shift)
                elif cast == 'string':
                    m.initial_value = '"{}"'.format(m.name)
            elif cast == 'int':
                # TODO if initialization is as enumerate of others members need throw error (example: one|two)
                values.append(m.initial_value)
            else:
                m.initial_value = 'None'

            shift += 1
        value = Object()
        value.initial_value = '{}::{}'.format(cls.name, cls.members[0].name)
        value.name = '_value'
        value.type = cast
        value.access = AccessSpecifier.private
        cls.members.append(value)
        return values

    @staticmethod
    def add_imports(cls_owner, func, model):
        # if not func:
        #     return func
        # if 'DataStorage' in func:
        #     func = 'from .DataStorage import DataStorage\n' + func
        # if RegexPatternPython.FACTORY.search(func):
        #     func = 'from .Factory import Factory\n' + func
        # for cls in model.classes:
        #     if cls.name not in RegexPatternPython.regs_class_names:
        #         RegexPatternPython.regs_class_names[cls.name] = re.compile(r'\b{}\b'.format(cls.name))
        #     pattern = RegexPatternPython.regs_class_names[cls.name]
        #     need = cls.name != cls_owner.name
        #     need = need and pattern.search(func) is not None
        #     if need:
        #         func = 'from .{0} import {0}\n'.format(cls.name) + func
        # if 'math.' in func:
        #     func = 'import math\n' + func
        # if 'random.' in func:
        #     func = 'import random\n' + func
        return func

    @staticmethod
    def replace_by_regex(func, model, function_args):
        function_args = ', '.join(['$' + x[0] for x in function_args])

        if not func and not function_args:
            return func

        strings = []
        string_pattern = '@{__string_%d__}'
        while '"' in func:
            left = func.index('"')
            right = left + 1
            p = ''
            while right < len(func):
                if func[right] == '"' and p != '\\':
                    string = func[left:right + 1]
                    func = func[:left] + string_pattern % len(strings) + func[right + 1:]
                    strings.append(string)
                    break
                p = func[right]
                right += 1

        for reg in RegexPatternPhp.FUNCTION:
            func = reg[0].sub(reg[1], func)

        for key in RegexPatternPhp.VARIABLES:
            patterns_dict = RegexPatternPhp.VARIABLES[key]
            arr = key.findall(function_args + '\n' + func)
            dividers = ' +-*\\=()[]<>\t\n!,.;'
            for var in arr:
                for ch in dividers:
                    i = 0
                    while i < len(func):
                        replace = False
                        full = ch + var
                        start = func.find(full, i)
                        if start == -1:
                            break
                        n = start + len(full)
                        i = n
                        if n < len(func):
                            replace = func[n] in dividers
                        if not replace:
                            continue
                        # func = func.replace(ch + var, ch + '$' + var)
                        func = func[:start] + (ch + '$' + var) + func[n:]

                pattern = '^' + var
                if pattern not in patterns_dict:
                    patterns_dict[pattern] = re.compile(pattern)
                pattern = patterns_dict[pattern]

                func = pattern.sub('$' + var, func)
                for ch in ['->']:
                    func = func.replace(ch + '$' + var, ch + var)

        for reg in RegexPatternPhp.FUNCTION_2:
            func = reg[0].sub(reg[1], func)

        for reg in RegexPatternPhp.REPLACES:
            func = func.replace(reg[0], reg[1])

        for i, string in enumerate(strings):
            func = func.replace(string_pattern % i, string)

        for cls in model.classes:
            if cls.name in func:
                func = 'require_once "{}.php";\n'.format(cls.name) + func

        return func
