from ..core.function import Function
from ..core.object import Objects


class GeneratorOperatorValueOf(object):

    def __init__(self):
        self.model = None

    def generate(self, model):
        self.model = model
        for cls in model.classes:
            GeneratorOperatorValueOf.add_value_of(cls)

    @staticmethod
    def add_value_of(class_):
        if class_.is_inline:
            return
        for method in class_.functions:
            if method.name == 'valueOf':
                return
        method = Function()
        method.name = 'valueOf'
        method.return_type = Objects.STRING
        method.operations.append('return Factory.serialize_command_to_json(this);')
        class_.functions.append(method)