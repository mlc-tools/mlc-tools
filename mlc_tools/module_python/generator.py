from ..base.generator import GeneratorBase
from ..base.generator_visitor import GeneratorVisitor
from ..core.class_ import Class
from .generator_data_storage import GeneratorDataStorage
from .generator_factory import GeneratorFactory
from .generator_package import GeneratorPackage
from .generator_observer import GeneratorObserver
from .generator_operator_equals import GeneratorOperatorEquals
from .generator_predefined_files import GeneratorPredefinedFiles


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model):
        self.generate_base_enum_class(model)
        GeneratorBase.generate(self, model)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model, False)
        GeneratorFactory().generate(model)
        GeneratorPackage().generate(model)
        GeneratorObserver().generate(model)
        GeneratorOperatorEquals().generate(model)
        GeneratorPredefinedFiles().generate(model)

    def generate_base_enum_class(self, model):
        base_enum = Class()
        base_enum.name = 'BaseEnum'
        base_enum.type = 'class'
        model.add_class(base_enum)
