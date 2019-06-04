from ..base.parser import Parser
from ..core.class_ import Class
from ..core.object import Object, Objects, AccessSpecifier
from ..core.function import Function


class GeneratorUnitTestsInterface(object):

    def __init__(self):
        self.tests = []
        self.model = None
        self.tests_interface_methods_count = 0
        self.tests_implemented_methods_count = 0

    def generate(self, model):
        self.model = model
        tests = []
        for cls in model.classes:
            test = self.generate_test_interface(cls)
            if test:
                tests.append(test)
        self.generate_base_classes()
        model.add_classes(tests)
        model.add_class(self.generate_all_tests_class())

    def generate_base_classes(self):
        base = BASE_CLASSES
        base = base.replace('@{all_methods}', str(self.tests_interface_methods_count))
        base = base.replace('@{implemented_methods}', str(self.tests_implemented_methods_count))
        self.model.parser.parse_text(base)

    @staticmethod
    def get_member_name(cls_name):
        name_ = ''
        for i, char in enumerate(cls_name):
            if char.isupper() and i > 0:
                name_ += '_'
            name_ += char.lower()
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

        if self.model.has_class(test.name[1:]):
            impl = self.model.get_class(test.name[1:])
            for func in impl.functions:
                if func.name.startswith('test_') and func.name not in generated_functions:
                    self.add_method(test, func.name)
                else:
                    self.tests_implemented_methods_count += 1

        if not test.functions:
            return None

        method = Function()
        method.name = 'execute'
        method.return_type = Objects.VOID
        test.functions.append(method)
        for func in test.functions:
            name = func.name
            if name == 'initialize' or name == 'execute':
                continue
            method.operations.append('this->{}();'.format(name))

        self.tests.append(test)
        return test

    @staticmethod
    def add_method(class_, name):
        method = Function()
        method.name = name
        method.return_type = Objects.VOID
        method.is_abstract = True
        class_.functions.append(method)

    def generate_all_tests_class(self,):
        test_all = Class()
        test_all.type = 'class'
        test_all.name = 'RunAllTests'
        test_all.group = 'tests'

        for test in self.tests:
            if self.model.has_class(test.name[1:]):
                var_name = self.get_member_name(test.name[1:])
                member = Object()
                member.type = test.name[1:]
                member.name = var_name
                test_all.members.append(member)

        method = Function()
        method.name = 'initialize'
        method.args.append(['logger', Parser.create_object('Logger*')])
        method.return_type = Objects.VOID
        test_all.functions.append(method)
        for test in test_all.members:
            var_name = self.get_member_name(test.name)
            method.operations.append('this->{}.initialize(logger);'.format(var_name))

        method = Function()
        method.name = 'execute'
        method.return_type = Objects.BOOL
        test_all.functions.append(method)
        for test in test_all.members:
            var_name = self.get_member_name(test.name)
            method.operations.append('this->{0}.execute();'.format(var_name))

        method.operations.append('bool result = true;')
        for test in test_all.members:
            var_name = self.get_member_name(test.name)
            method.operations.append('result = result && this->{0}.result;'.format(var_name))
        method.operations.append('return result;')

        return test_all


BASE_CLASSES = '''
class tests/Logger<SerializedObject>:test:virtual
{
    int tests_count
    int success_count
    int class_count = 0
    int methods_count = 0
    int all_methods_count = @{all_methods}
    int implemented_methods_count = @{implemented_methods}
    
    function void message(string message):abstract
    function void log(string message)
    {
        this->message(message);
    }
}

class tests/TestCase<SerializedObject>:test
{
    Logger*:runtime logger
    bool:runtime result = true

    function void initialize(Logger* logger)
    {
        this->logger = logger;
    }
    function void execute():abstract
    function void add_result(bool result, string message):private
    {
        if(this->result && !result)
        {
            this->logger->message(this->get_type() + ":");
        }
        if(!result)
        {
            this->logger->message(" - Failed: " + message);
        }
        this->result = this->result && result;
    }
    function void assertTrue(bool expression, string message="")
    {
        this->add_result(expression, message);
    }
    function void assertFalse(bool expression, string message="")
    {
        this->add_result(!expression, message);
    }
    function<T> void assertEqual(T left, T right, string message="")
    {
        this->add_result(left == right, message);
    }
    function<T> void assertNotEqual(T left, T right, string message="")
    {
        this->add_result(left != right, message);
    }
    function<T> void assertNull(T value, string message="")
    {
        this->add_result(value == nullptr, message);
    }
    function<T> void assertNotNull(T value, string message="")
    {
        this->add_result(value != nullptr, message);
    }
    function<Key, Value> void assertInMap(Key key, map<Key, Value>:const:ref map, string message="")
    {
        this->add_result(in_map(key, map), message);
    }
    function<Key, Value> void assertNotInMap(Key key, map<Key, Value>:const:ref map, string message="")
    {
        this->add_result(!in_map(key, map), message);
    }
    function<T> void assertInList(T item, list<T>:const:ref list, string message="")
    {
        this->add_result(in_list(item, list), message);
    }
    function<T> void assertNotInList(T item, list<T>:const:ref list, string message="")
    {
        this->add_result(!in_list(item, list), message);
    }
    function<T> void assertInRange(T value, T min_value, T max_value, string message="")
    {
        bool result = value >= min_value && value <= max_value;
        this->add_result(result, message);
    }
    function<T> void assertNotInRange(T value, T min_value, T max_value, string message="")
    {
        bool result = value < min_value || value > max_value;
        this->add_result(result, message);
    }
}
'''
