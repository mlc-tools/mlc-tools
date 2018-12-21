from ..core.object import Object, AccessSpecifier


class TranslatorBase(object):

    def __init__(self):
        pass

    def translate(self, model):
        for cls in model.classes:
            if cls.type == 'enum':
                self.convert_to_enum(cls)
            for method in cls.functions:
                self.translate_function(cls, method, model)

    def translate_function(self, cls, method, model):
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
            elif cast == 'int':
                # TODO if initialization is as enumerate of others members need throw error (example: one|two)
                values.append(member.initial_value)
            else:
                member.initial_value = 'None'

            shift += 1
        value = Object()
        value.initial_value = '{}::{}'.format(cls.name, cls.members[0].name)
        value.name = '_value'
        value.type = cast
        value.access = AccessSpecifier.private
        cls.members.append(value)
        return values