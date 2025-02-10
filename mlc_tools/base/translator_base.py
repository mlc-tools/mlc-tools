

class TranslatorBase(object):

    def __init__(self):
        pass

    def translate(self, model):
        for cls in model.classes:
            for member in cls.members:
                if member.type == 'Observable':
                    member.is_runtime = True
                else:
                    for t in member.template_args:
                        if t.type == 'Observable':
                            member.is_runtime = True
                            break

            if cls.type == 'enum':
                self.convert_to_enum(cls)
            for method in cls.functions:
                self.translate_function(cls, method, model)

    def translate_function(self, cls, method, model):
        if not method.translated:
            body = '\n'.join(method.operations)
            body = self.translate_function_body(cls, method, body, model, method.args)
            method.body = body
        elif method.operations:
            method.body = '\n'.join(method.operations)

    def translate_function_body(self, cls, func, body, model, args):
        func = self.replace_by_regex(func, body, model, args)
        return func

    def replace_by_regex(self, func, body, model, args):
        pass

    def convert_to_enum(self, cls):
        shift = 0
        cast = 'string'
        values = []
        for member in cls.members:
            if member.name:
                continue
            member.name = member.type
            member.type = cast
            member.is_static = True
            member.is_const = True
            if member.initial_value is None:
                if cast == 'int':
                    member.initial_value = '(1 << {})'.format(shift)
                    values.append(1 << shift)
                elif cast == 'string':
                    member.initial_value = '"{}"'.format(member.name)
            else:
                # TODO if initialization is as enumerate of others members need throw error (example: one|two)
                cast = 'int'
                values.append(member.initial_value)

            shift += 1
        return values

    @staticmethod
    def replace(text, pattern):
        skip = len(pattern) > 2
        filters = pattern[2] if len(pattern) > 2 else []
        for filter_ in filters:
            skip = skip and text.find(filter_) == -1
        if not skip:
            text = pattern[0].sub(pattern[1], text)
        return text

    @staticmethod
    def save_strings(func):
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
        return func, strings

    @staticmethod
    def restore_strings(func, strings):
        string_pattern = '@{__string_%d__}'
        for i, string in enumerate(strings):
            func = func.replace(string_pattern % i, string)
        return func
