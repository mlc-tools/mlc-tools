from ..base.generator import GeneratorBase
from ..base.generator_visitor import GeneratorVisitor
from .generator_data_storage import GeneratorDataStorage
from .generator_factory import GeneratorFactory
from .generator_package import GeneratorPackage
from .generator_observer import GeneratorObserver
from .generator_operator_equals import GeneratorOperatorEquals


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model):
        GeneratorBase.generate(self, model)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model, False)
        GeneratorFactory().generate(model)
        GeneratorPackage().generate(model)
        GeneratorObserver().generate(model)
        GeneratorOperatorEquals().generate(model)
