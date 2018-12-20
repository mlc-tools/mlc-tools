from .generator_unit_tests_interface import GeneratorUnitTestsInterface


class GeneratorBase(object):

    def __init__(self):
        pass

    def generate(self, model, writer):
        if model.generate_tests:
            GeneratorUnitTestsInterface().generate(model)
