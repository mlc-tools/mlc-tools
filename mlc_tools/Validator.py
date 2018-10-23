from .Error import Error


class Validator:
    def __init__(self):
        pass
    
    def validate(self, parser):
        self.validate_php_functional(parser)
    
    @staticmethod
    def validate_php_functional(parser):
        for cls in parser.classes:
            for member in cls.members:
                if member.type == 'map':
                    key_type = member.template_args[0]
                    key_type = key_type if isinstance(key_type, str) else key_type.type
                    cls_type = parser.find_class(key_type)
                    if cls_type is not None and cls_type.type != 'enum':
                        value_type = member.template_args[1] if isinstance(member.template_args[1], str) else \
                        member.template_args[1].type
                        Error.exit(Error.OBJECT_IS_KEY_OF_MAP, cls.name, key_type, value_type, member.name)
                if cls.type == 'enum' and member.initial_value is not None:
                    if '|' in member.initial_value or \
                                    '&' in member.initial_value or \
                                    '^' in member.initial_value or \
                                    '~' in member.initial_value:
                        Error.exit(Error.ENUM_CANNOT_BE_COMBINATED, cls.name, member.name, member.initial_value)
