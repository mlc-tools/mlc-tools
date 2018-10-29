from ..base.Generator import *
from .GeneratorDataStorage import GeneratorDataStorage
from .GeneratorVisitor import GeneratorVisitor
from .GeneratorPredefinedFiles import GeneratorPredefinedFiles
from .GeneratorOperatorEquals import GeneratorOperatorEquals
from .GeneratorObserver import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, parser, writer):
        GeneratorBase.generate(self, parser, writer)
        GeneratorDataStorage().generate(parser)
        GeneratorVisitor().generate(parser)
        GeneratorPredefinedFiles().generate(writer)
        GeneratorOperatorEquals().generate(parser)
        GeneratorObserver().generate(writer)
