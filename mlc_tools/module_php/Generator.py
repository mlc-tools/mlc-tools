from ..base.Generator import *
from .GeneratorDataStorage import GeneratorDataStorage
from .GeneratorVisitor import GeneratorVisitor
from .GeneratorFactory import GeneratorFactory
from .GeneratorObserver import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, parser, writer):
        GeneratorBase.generate(self, parser, writer)
        GeneratorDataStorage().generate(parser)
        GeneratorVisitor().generate(parser)
        GeneratorFactory().generate(parser, writer)
        GeneratorObserver().generate(writer)
