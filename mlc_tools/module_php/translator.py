import re
from .regex import RegexPatternPhp
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def replace_by_regex(self, func, model, args):
        args = ', '.join(['$' + x[0] for x in args])

        if not func and not args:
            return func

        func, strings = self.save_strings(func)

        for reg in RegexPatternPhp.FUNCTION:
            func = self.replace(func, reg)

        for key in RegexPatternPhp.VARIABLES:
            patterns_dict = RegexPatternPhp.VARIABLES[key]
            arr = key.findall(args + '\n' + func)
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

        func = self.restore_strings(func, strings)

        for cls in model.classes:
            if cls.name in func:
                func = 'require_once "{}.php";\n'.format(cls.name) + func

        return func
