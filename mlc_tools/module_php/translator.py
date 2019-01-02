import re
from .regex import RegexPatternPhp
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
            if method.operations:
                method.body = '\n        '.join(method.operations)

    def translate_function_body(self, class_, func, model, args):
        func = self.replace_by_regex(func, model, args)
        func = Translator.add_imports(class_, func, model)
        return func

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

    def replace_by_regex(self, func, model, function_args):
        function_args = ', '.join(['$' + x[0] for x in function_args])

        if not func and not function_args:
            return func

        strings = []
        string_pattern = '@{__string_%d__}'
        while '"' in func:
            left = func.index('"')
            right = left + 1
            char = ''
            while right < len(func):
                if func[right] == '"' and char != '\\':
                    string = func[left:right + 1]
                    func = func[:left] + string_pattern % len(strings) + func[right + 1:]
                    strings.append(string)
                    break
                char = func[right]
                right += 1

        for reg in RegexPatternPhp.FUNCTION:
            func = self.replace(func, reg)

        for key in RegexPatternPhp.VARIABLES:
            patterns_dict = RegexPatternPhp.VARIABLES[key]
            arr = key.findall(function_args + '\n' + func)
            dividers = ' +-*\\=()[]<>\t\n!,.;'
            for var in arr:
                for char in dividers:
                    i = 0
                    while i < len(func):
                        replace = False
                        full = char + var
                        start = func.find(full, i)
                        if start == -1:
                            break
                        position = start + len(full)
                        i = position
                        if position < len(func):
                            replace = func[position] in dividers
                        if not replace:
                            continue
                        # func = func.replace(ch + var, ch + '$' + var)
                        func = func[:start] + (char + '$' + var) + func[position:]

                pattern = '^' + var
                if pattern not in patterns_dict:
                    patterns_dict[pattern] = re.compile(pattern)
                pattern = patterns_dict[pattern]

                func = pattern.sub('$' + var, func)
                for char in ['->']:
                    func = func.replace(char + '$' + var, char + var)

        for reg in RegexPatternPhp.FUNCTION_2:
            func = self.replace(func, reg)

        for reg in RegexPatternPhp.REPLACES:
            func = func.replace(reg[0], reg[1])

        for i, string in enumerate(strings):
            func = func.replace(string_pattern % i, string)

        for cls in model.classes:
            if cls.name in func:
                func = 'require_once "{}.php";\n'.format(cls.name) + func

        return func
