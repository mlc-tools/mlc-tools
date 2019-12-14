from .regex import RegexPatternJs
from ..base.translator_base import TranslatorBase


class Translator(TranslatorBase):

    def __init__(self):
        TranslatorBase.__init__(self)

    def replace_by_regex(self, func, body, model, args):
        args = ', '.join([x[0] for x in args])
        if not body and not args:
            return body
        body, strings = self.save_strings(body)
        for reg in RegexPatternJs.FUNCTION:
            body = self.replace(body, reg)
        for reg in RegexPatternJs.REPLACES:
            body = body.replace(reg[0], reg[1])
        body = self.restore_strings(body, strings)

        return body
