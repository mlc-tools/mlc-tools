from .regex import RegexPatternJs
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def replace_by_regex(self, func, model, args):
        args = ', '.join([x[0] for x in args])
        if not func and not args:
            return func
        func, strings = self.save_strings(func)
        for reg in RegexPatternJs.FUNCTION:
            func = self.replace(func, reg)
        for reg in RegexPatternJs.REPLACES:
            func = func.replace(reg[0], reg[1])
        func = self.restore_strings(func, strings)

        return func
