from ..utils.error import Error


class Validator(object):

    def __init__(self):
        pass

    def validate(self, model):
        self.validate_php_functional(model)

    @staticmethod
    def validate_php_functional(model):
        for cls in model.classes:
            for member in cls.members:
                if member.type == 'map':
                    key_type = member.template_args[0].type
                    if model.has_class(key_type) and model.get_class(key_type).type != 'enum' and model.php_validate:
                        value_type = member.template_args[1].type
                        Error.exit(Error.OBJECT_IS_KEY_OF_MAP, cls.name, key_type, value_type, member.name)
                if cls.type == 'enum' and member.initial_value is not None:
                    if '|' in member.initial_value or \
                            '&' in member.initial_value or \
                            '^' in member.initial_value or \
                            '~' in member.initial_value:
                        Error.exit(Error.ENUM_CANNOT_BE_COMBINATED, cls.name, member.name, member.initial_value)
