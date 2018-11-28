from ..base.Generator import *
from .GeneratorDataStorage import GeneratorDataStorage
from .GeneratorVisitor import GeneratorVisitor
from .GeneratorFactory import GeneratorFactory
from .GeneratorPackage import GeneratorPackage
from .GeneratorObserver import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model, writer):
        GeneratorBase.generate(self, model, writer)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model)
        GeneratorFactory().generate(model, writer)
        GeneratorPackage().generate(model, writer)
        GeneratorObserver().generate(writer)
