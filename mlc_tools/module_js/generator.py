from .generator_predefined_files import GeneratorPredefinedFiles
from ..base.generator import GeneratorBase
from ..base.generator_visitor import GeneratorVisitor
from .generator_data_storage import GeneratorDataStorage
from .generator_factory import GeneratorFactory
from .generator_observer import GeneratorObserver
from .generator_config import GeneratorConfig
from .generator_operator_value_of import GeneratorOperatorValueOf
from .generator_functions import GeneratorFunctions
from ..core.class_ import Class


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model):
        self.generate_base_enum_class(model)
        GeneratorBase.generate(self, model)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model, False)
        GeneratorFactory().generate(model)
        GeneratorObserver().generate(model)
        GeneratorConfig().generate(model)
        GeneratorOperatorValueOf().generate(model)
        GeneratorFunctions.generate(model)
        GeneratorPredefinedFiles().generate(model)

    def generate_base_enum_class(self, model):
        base_enum = Class()
        base_enum.name = 'BaseEnum'
        base_enum.type = 'class'
        model.add_class(base_enum)
