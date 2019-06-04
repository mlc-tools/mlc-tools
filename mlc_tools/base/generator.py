from .generator_unit_tests_interface import GeneratorUnitTestsInterface


# pylint: disable=no-self-use
# pylint: disable=unused-argument
class GeneratorBase(object):

    def __init__(self):
        pass

    def generate(self, model):
        if model.generate_tests:
            GeneratorUnitTestsInterface().generate(model)
