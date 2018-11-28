from ..base.Generator import *
from .GeneratorDataStorage import GeneratorDataStorage
from .GeneratorVisitor import GeneratorVisitor
from .GeneratorPredefinedFiles import GeneratorPredefinedFiles
from .GeneratorOperatorEquals import GeneratorOperatorEquals
from .GeneratorObserver import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model, writer):
        GeneratorBase.generate(self, model, writer)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model)
        GeneratorPredefinedFiles().generate(model, writer)
        GeneratorOperatorEquals().generate(model)
        GeneratorObserver().generate(writer)
