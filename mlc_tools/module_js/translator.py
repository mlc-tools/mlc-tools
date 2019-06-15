from .regex import RegexPatternJs
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
            method.body = '\n'.join(method.operations)

    def translate_function_body(self, _, func, model, args):
        func = self.replace_by_regex(func, model, args)
        return func

    def replace_by_regex(self, func, _, function_args):
        function_args = ', '.join([x[0] for x in function_args])

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

        for reg in RegexPatternJs.FUNCTION:
            func = self.replace(func, reg)

        for reg in RegexPatternJs.REPLACES:
            func = func.replace(reg[0], reg[1])

        for i, string in enumerate(strings):
            func = func.replace(string_pattern % i, string)

        return func
