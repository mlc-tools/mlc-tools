from .GeneratorUnitTestsInterface import GeneratorUnitTestsInterface


class GeneratorBase:

    def __init__(self):
        pass

    def generate(self, model, writer):
        GeneratorUnitTestsInterface().generate(model)
