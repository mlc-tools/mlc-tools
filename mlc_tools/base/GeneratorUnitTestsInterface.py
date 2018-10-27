from ..core.Class import Class
from ..core.Object import Object, AccessSpecifier
from ..core.Function import Function


class GeneratorUnitTestsInterface:

    def __init__(self):
        self.tests = []
        self.parser = None
        self.tests_interface_methods_count = 0
        self.tests_implemented_methods_count = 0

    def generate(self, parser):
        self.parser = parser
        tests = []
        for cls in parser.classes:
            test = self.generate_test_interface(cls)
            if test:
                tests.append(test)
        self.generate_base_classes()
        parser.classes.extend(tests)
        parser.classes.append(self.generate_all_tests_class())

    def generate_base_classes(self):
        base = base_classes
        base = base.replace('@{all_methods}', str(self.tests_interface_methods_count))
        base = base.replace('@{implemented_methods}', str(self.tests_implemented_methods_count))
        self.parser.parse(base)

    @staticmethod
    def get_member_name(cls_name):
        name_ = ''
        for i, ch in enumerate(cls_name):
            if ch.isupper() and i > 0:
                name_ += '_'
            name_ += ch.lower()
        return name_

    def generate_test_interface(self, cls):
        if cls.is_test:
            return None
        test = Class()
        test.type = 'class'
        test.name = 'ITest' + cls.name
        test.group = 'tests'
        test.superclasses.append('TestCase')
        generated_functions = []
        for func in cls.functions:
            ignored = ['visit', 'accept']
            if func.name not in ignored and func.access == AccessSpecifier.public:
                self.add_method(test, 'test_' + func.name)
                generated_functions.append('test_' + func.name)
                self.tests_interface_methods_count += 1

        impl = self.parser.find_class(test.name[1:])
        if impl:
            for func in impl.functions:
                if func.name.startswith('test_') and func.name not in generated_functions:
                    self.add_method(test, func.name)
                else:
                    self.tests_implemented_methods_count += 1

        if len(test.functions) == 0:
            return None

        method = Function()
        method.name = 'execute'
        method.return_type = 'bool'
        test.functions.append(method)
        method.operations.append('bool result = true;')
        for func in test.functions:
            name = func.name
            if name == 'initialize' or name == 'execute':
                continue
            method.operations.append('result = this->{0}();'.format(name, name[5:]))
            method.operations.append('this->logger->push(result, " - [{1}] tested");'.format(name, name[5:]))
            method.operations.append(
                'this->logger->push(result, "---------------------------------------------------------");')
            method.operations.append('this->logger->methods_count += 1;')
            method.operations.append('if(!result)')
            method.operations.append('{')
            method.operations.append('    exit(1);')
            method.operations.append('}')

        method.operations.append('return this->logger->result;')

        self.tests.append(test)
        return test

    @staticmethod
    def add_method(cls, name):
        method = Function()
        method.name = name
        method.return_type = 'bool'
        method.is_abstract = True
        cls.functions.append(method)

    def generate_all_tests_class(self,):
        test_all = Class()
        test_all.type = 'class'
        test_all.name = 'RunAllTests'
        test_all.group = 'tests'
        test_all.superclasses.append('TestCase')

        for test in self.tests:
            if self.parser.find_class(test.name[1:]):
                var_name = self.get_member_name(test.name[1:])
                member = Object()
                member.type = test.name[1:]
                member.name = var_name
                test_all.members.append(member)

        method = Function()
        method.name = 'initialize'
        method.args.append(['logger', 'Logger*'])
        method.return_type = 'void'
        test_all.functions.append(method)
        method.operations.append('this->logger = logger;')
        for test in test_all.members:
            var_name = self.get_member_name(test.name)
            method.operations.append('this->{}.initialize(logger);'.format(var_name))

        method = Function()
        method.name = 'execute'
        method.return_type = 'bool'
        test_all.functions.append(method)
        for test in test_all.members:
            var_name = self.get_member_name(test.name)
            method.operations.append('this->logger->push(true, "Test case [\" + this->{0}.get_type() + \"] started");'.
                                     format(var_name))
            method.operations.append('this->logger->push(this->{0}.execute(), '
                                     '"Test case [\" + this->{0}.get_type() + \"] finished\\n");'.format(var_name))
            method.operations.append('this->logger->class_count += 1;')
        method.operations.append('return this->logger->result;')

        return test_all


base_classes = '''
class tests/Logger<SerializedObject>:test
{
    bool result = true
    int tests_count
    int success_count
    int class_count = 0
    int methods_count = 0
    int all_methods_count = @{all_methods}
    int implemented_methods_count = @{implemented_methods}
    
    function bool push(bool result, string message)
    {
        this->tests_count += 1;
        if(result)
            this->success_count += 1;
        this->result = this->result && result;
        this->print_log(result, message);
        return result;
    }
    function void print_log(bool result, string message):abstract
}

class tests/TestCase<SerializedObject>:test
{
    Logger*:runtime logger

    function void initialize(Logger* logger)
    {
        this->logger = logger;
    }
    function bool execute()
    {
        return false;
    }
}
'''
