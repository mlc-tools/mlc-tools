from ..base.generator import *
from .generator_data_storage import GeneratorDataStorage
from .generator_visitor import GeneratorVisitor
from .generator_factory import GeneratorFactory
from .generator_observer import GeneratorObserver


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate(self, model, writer):
        GeneratorBase.generate(self, model, writer)
        GeneratorDataStorage().generate(model)
        GeneratorVisitor().generate(model)
        GeneratorFactory().generate(model, writer)
        GeneratorObserver().generate(writer)
