from mlc_tools.module_cpp.generator_ref_counter import GeneratorRefCounter
from ..base.generator import GeneratorBase
from .generator_data_storage import GeneratorDataStorage
from ..base.generator_visitor import GeneratorVisitor
from .generator_predefined_files import GeneratorPredefinedFiles
from .generator_operator_equals import GeneratorOperatorEquals
from .generator_observer import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model):
        GeneratorBase.generate(self, model)
        GeneratorDataStorage().generate(model)
        GeneratorPredefinedFiles().generate(model)
        GeneratorVisitor().generate(model, True)
        GeneratorObserver().generate(model)
        GeneratorRefCounter().generate(model)
        GeneratorOperatorEquals().generate(model)
