from Class import Class
from Object import Object
from Function import Function


class Test:

    def __init__(self, parser):
        self.tests = []
        self.parser = parser

    def generate_test_interface(self, cls):
        if len(cls.functions) == 0 or cls.is_test:
            return None
        test = Class()
        test.type = 'class'
        test.name = 'ITest' + cls.name
        test.group = 'tests'
        test.behaviors.append('TestCase')
        generated_functions = []
        for func in cls.functions:
            ignored = ['visit']
            if func.name not in ignored:
                self.add_function(test, 'test_' + func.name)
                generated_functions.append('test_' + func.name)

        impl = self.parser.find_class(test.name[1:])
        if impl:
            for func in impl.functions:
                if func.name.startswith('test_') and func.name not in generated_functions:
                    self.add_function(test, func.name)

        if len(test.functions) == 0:
            return None

        function = Function()
        function.name = 'execute'
        function.return_type = 'bool'
        test.functions.append(function)
        for func in test.functions:
            name = func.name
            if name == 'initialize' or name == 'execute':
                continue
            function.operations.append('this->logger->add_result(this->{0}(), " - [{1}] tested");'.format(name, name[5:]))
            function.operations.append('this->logger->add_result(true, "---------------------------------------------------------");'.format(name, name[5:]))

        function.operations.append('return this->logger->result;')

        self.tests.append(test)
        return test

    def add_function(self, cls, name):
        function = Function()
        function.name = name
        function.return_type = 'bool'
        function.is_abstract = True
        cls.functions.append(function)

    def generate_all_tests_class(self,):
        test_all = Class()
        test_all.type = 'class'
        test_all.name = 'RunAllTests'
        test_all.group = 'tests'
        test_all.behaviors.append('TestCase')

        for test in self.tests:
            if self.parser.find_class(test.name[1:]):
                var_name = test.name[1:]
                member = Object()
                member.type = test.name[1:]
                member.name = var_name
                test_all.members.append(member)

        function = Function()
        function.name = 'initialize'
        function.args.append(['logger', 'Logger*'])
        function.return_type = 'void'
        test_all.functions.append(function)
        function.operations.append('this->logger = logger;')
        for test in test_all.members:
            var_name = test.name
            function.operations.append('this->{}.initialize(logger);'.format(var_name))

        function = Function()
        function.name = 'execute'
        function.return_type = 'bool'
        test_all.functions.append(function)
        for test in test_all.members:
            var_name = test.name
            function.operations.append('this->logger->add_result(true, "Test case [\" + this->{0}.get_type() + \"] started");'.format(var_name))
            function.operations.append(
                'this->logger->add_result(this->{0}.execute(), "Test case [\" + this->{0}.get_type() + \"] finished\\n");'.format(var_name))
        function.operations.append('return this->logger->result;')

        return test_all
