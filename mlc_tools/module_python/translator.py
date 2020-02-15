import re
from .regex import RegexPatternPython
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def translate_function(self, cls, method, model):
        if not method.translated:
            body = '\n'.join(method.operations)
            body = self.translate_function_body(cls, method, body, model, method.args)
            method.body = body
        else:
            if method.operations:
                method.body = '\n        '.join(method.operations)
            else:
                method.body = 'pass'

    def translate_function_body(self, cls, method, body, model, args):
        if not body:
            body = 'pass'
        body = self.replace_by_regex(method, body, model, args)
        body = Translator.convert_braces_to_tabs(body)
        body = Translator.remove_double_eol(body)
        body = Translator.add_imports(cls, body, model)
        return body

    @staticmethod
    def add_imports(cls_owner, func, model):
        if not func:
            return func
        imports = []
        if RegexPatternPython.FACTORY.search(func):
            imports.append('from .Factory import Factory')
        for cls in model.classes:
            if cls.name in func:
                need = cls.name is not cls_owner.name
                if not need:
                    continue
                pattern = None
                if cls.name not in RegexPatternPython.regs_class_names:
                    pattern = re.compile(r'\b{}\b'.format(cls.name))
                    RegexPatternPython.regs_class_names[cls.name] = pattern
                pattern = pattern or RegexPatternPython.regs_class_names[cls.name]
                need = need and pattern.search(func) is not None
                if need:
                    imports.append('from .{0} import {0}'.format(cls.name))
        if 'math.' in func:
            imports.append('import math')
        if 'random.' in func:
            imports.append('import random')
        if imports:
            imports = Translator.get_tabs(2) + '\n{}'.format(Translator.get_tabs(2)).join(imports)
            func = '{}\n{}'.format(imports, func)
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

    def replace_by_regex(self, func, body, model, args):
        if not body:
            return body
        for reg in RegexPatternPython.FUNCTION:
            body = self.replace(body, reg)
        for reg in RegexPatternPython.REPLACES:
            body = body.replace(reg[0], reg[1])
        return body

    @staticmethod
    def get_tabs(count):
        return '    ' * count
