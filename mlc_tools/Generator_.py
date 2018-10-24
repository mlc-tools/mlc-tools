from .TestClass import GeneratorTestInterfaces

class Generator:
    def __init__(self):
        self.parser = None
        self.base_visitor_classes = {}
    
    def generate_tests_interfaces(self, parser):
        self.parser = parser
        generator = GeneratorTestInterfaces(parser)
        tests = []
        for cls in parser.classes:
            test = generator.generate_test_interface(cls)
            if test:
                tests.append(test)
        generator.generate_base_classes()
        parser.classes.extend(tests)
        parser.classes.append(generator.generate_all_tests_class())
