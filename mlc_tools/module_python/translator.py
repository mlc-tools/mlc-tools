import re
from .regex import RegexPatternPython
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def translate_function(self, cls, method, model):
        if not method.translated:
            body = '\n'.join(method.operations)
            body = self.translate_function_body(cls, body, model)
            method.body = body
        else:
            if method.operations:
                method.body = '\n        '.join(method.operations)
            else:
                method.body = 'pass'

    def translate_function_body(self, class_, func, model):
        if not func:
            func = 'pass'
        func = self.replace_by_regex(func)
        func = Translator.convert_braces_to_tabs(func)
        func = Translator.remove_double_eol(func)
        func = Translator.add_imports(class_, func, model)
        return func

    @staticmethod
    def add_imports(cls_owner, func, model):
        if not func:
            return func
        if 'DataStorage' in func:
            func = Translator.get_tabs(2) + 'from .DataStorage import DataStorage\n' + func
        if RegexPatternPython.FACTORY.search(func):
            func = Translator.get_tabs(2) + 'from .Factory import Factory\n' + func
        for cls in model.classes:
            if cls.name in func:
                if cls.name not in RegexPatternPython.regs_class_names:
                    RegexPatternPython.regs_class_names[cls.name] = re.compile(r'\b{}\b'.format(cls.name))
                pattern = RegexPatternPython.regs_class_names[cls.name]
                need = cls.name != cls_owner.name
                need = need and pattern.search(func) is not None
                if need:
                    func = Translator.get_tabs(2) + 'from .{0} import {0}\n'.format(cls.name) + func
        if 'math.' in func:
            func = Translator.get_tabs(2) + 'import math\n' + func
        if 'random.' in func:
            func = Translator.get_tabs(2) + 'import random\n' + func
        return func

    @staticmethod
    def remove_double_eol(func):
        if not func:
            return func
        func = func.replace('\n    \n', '\n')
        func = func.replace('\n        \n', '\n')
        func = func.replace('\n            \n', '\n')
        func = func.replace('\n                \n', '\n')
        func = func.replace('\n                    \n', '\n')
        func = func.replace('\n                        \n', '\n')
        return func

    @staticmethod
    def convert_braces_to_tabs(func):
        if not func:
            return func
        lines = func.split('\n')
        tabs = 2
        next_tab = False
        for i, line in enumerate(lines):
            if next_tab:
                tabs += 1
            if '{' in line:
                tabs += 1
                line = line.replace('{', '')
            if '}' in line:
                tabs -= 1
                line = line.replace('}', '')
            lines[i] = Translator.get_tabs(tabs) + line.strip()
            if next_tab:
                next_tab = False
                tabs -= 1
            if (line.startswith('for') or line.startswith('if') or line.startswith('else') or line.startswith('elif')
                    or line.startswith('try:') or line.strip().startswith('except')) \
                    and (i < len(lines) - 1 and '{' not in line and '{' not in lines[i + 1]):
                next_tab = True

        func = '\n'.join(lines)
        return func

    def replace_by_regex(self, func):
        if not func:
            return func
        for reg in RegexPatternPython.FUNCTION:
            func = self.replace(func, reg)
        for reg in RegexPatternPython.REPLACES:
            func = func.replace(reg[0], reg[1])
        return func

    @staticmethod
    def get_tabs(count):
        return '    ' * count
