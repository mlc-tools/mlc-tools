import re
from .regex import RegexPatternPhp
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def replace_by_regex(self, func, body, model, args_):
        args = []
        args.extend(args_)
        args.extend(func.template_types)
        args = ', '.join(['$' + x[0] for x in args])

        if not body and not args:
            return body

        body, strings = self.save_strings(body)

        for reg in RegexPatternPhp.FUNCTION:
            body = self.replace(body, reg)

        for key in RegexPatternPhp.VARIABLES:
            patterns_dict = RegexPatternPhp.VARIABLES[key]
            arr = key.findall(args + '\n' + body)
            dividers = ' +-*\\=()[]<>\t\n!,.;'
            for var in arr:
                for char in dividers:
                    i = 0
                    while i < len(body):
                        replace = False
                        full = char + var
                        start = body.find(full, i)
                        if start == -1:
                            break
                        position = start + len(full)
                        i = position
                        if position < len(body):
                            replace = body[position] in dividers
                        if not replace:
                            continue
                        # func = func.replace(ch + var, ch + '$' + var)
                        body = body[:start] + (char + '$' + var) + body[position:]

                pattern = '^' + var
                if pattern not in patterns_dict:
                    patterns_dict[pattern] = re.compile(pattern)
                pattern = patterns_dict[pattern]

                body = pattern.sub('$' + var, body)
                for char in ['->']:
                    body = body.replace(char + '$' + var, char + var)

        for reg in RegexPatternPhp.FUNCTION_2:
            body = self.replace(body, reg)

        for reg in RegexPatternPhp.REPLACES:
            body = body.replace(reg[0], reg[1])

        body = self.restore_strings(body, strings)

        for cls in model.classes:
            if cls.name in body:
                body = 'require_once "{}.php";\n'.format(cls.name) + body

        return body
