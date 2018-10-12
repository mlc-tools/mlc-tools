from copy import deepcopy

from .Object import Object
from .Class import Class
from .Function import Function
from .protocols import protocols
from .Error import Error
from .ObserverCreater import ObserverPatterGenerator
from .TestClass import Test
import sys


def _is_class(line):
    return line.strip().find('class') == 0


def _is_interface(line):
    return line.strip().find('interface') == 0


def _is_functon(line):
    return line.strip().find('function') == 0


def _is_enum(line):
    return line.strip().find('enum') == 0


def find_body(text):
    text = text.strip()
    body = ""
    if text.find("\n") != -1:
        header = text[0:text.find("\n")]
    else:
        header = text
    if header.find(':external') == -1 and header.find(':abstract') == -1:
        text = text[text.find("{"):]
        counter = 0
        index = 0
        for ch in text:
            index += 1
            if counter == 0 and ch == '{':
                counter += 1
                continue
            if ch == '{':
                counter += 1
            if ch == '}':
                counter -= 1
            if counter == 0:
                text = text[index:]
                break
            body += ch
    else:
        text = text[len(header):].strip()
    return body, header, text


class Parser:

    def __init__(self, side, generate_tests, generate_intrusive, generate_factory):
        self.classes = []
        self.classes_for_data = []
        self.objects = []
        self.functions = []
        self.side = side
        self.copyright_text = ''
        self.simple_types = ["int", "float", "bool", "string"]
        self.is_validate_php_features = True
        self.configs_root = ''
        self.generate_tests = generate_tests
        self.generate_intrusive = generate_intrusive
        self.generate_factory = generate_factory
        return

    def generate_patterns(self):
        self.classes.append(ObserverPatterGenerator.get_mock())

    def save_patterns(self, writer, language):
        ObserverPatterGenerator.generate(language, writer)

    def set_configs_directory(self, path):
        self.configs_root = path

    def is_side(self, side):
        return self.side == 'both' or side == self.side or side == 'both'

    def parse(self, text):
        text = text.strip()
        left = text.find('/*')
        while left != -1:
            right = text.find('*/')
            if right != -1:
                text = text[:left] + text[right + 2:]
            left = text.find('/*')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if '//' in line:
                lines[i] = line[0:line.find('//')]
        text = '\n'.join(lines)
        while len(text) > 0:
            text = text.strip()
            if _is_class(text):
                text = self._create_class(text, False)
            elif _is_interface(text):
                text = self._create_class(text, True)
            elif _is_enum(text):
                text = self._create_enum_class(text)
            elif _is_functon(text):
                text = self._create_function(text)
            else:
                text = self._create_declaration(text)

    def link(self):
        for function in self.functions:
            parts = function.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                function_name = parts[1]
                class_ = self.find_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_METHOD, class_name, function.name)
                function.name = function_name
                class_.functions.append(function)
        self.functions = []

        for object_ in self.objects:
            parts = object_.name.split('::')
            if len(parts) == 2:
                class_name = parts[0]
                object_name = parts[1]
                class_ = self.find_class(class_name)
                if class_ is None:
                    Error.exit(Error.CANNOT_FIND_CLASS_FOR_OBJECT, class_name, object_.name)
                object_.name = object_name
                class_.members.append(object_)
                self.objects.remove(object_)

        if self.generate_tests:
            generator = Test(self)
            tests = []
            for cls in self.classes:
                test = generator.generate_test_interface(cls)
                if test:
                    tests.append(test)
            generator.generate_base_classes()
            self.classes.extend(tests)
            self.classes.append(generator.generate_all_tests_class())

        for cls in self.classes:
            if cls.is_visitor and self.get_type_of_visitor(cls) != cls.name:
                if cls.name.find('IVisitor') != 0:
                    self.create_visitor_class(cls)

        for cls in self.classes:
            superclasses = []
            for name in cls.superclasses:
                c = self.find_class(name)
                if c is None:
                    Error.exit(Error.UNKNOWN_SUPERCLASS, cls.name, name)
                superclasses.append(c)
                c.subclasses.append(cls)
            cls.superclasses = superclasses

        for cls in self.classes:
            cls.is_serialized = self.is_serialised(cls)
            cls.is_visitor = self.is_visitor(cls)
            if cls.is_visitor and cls.name != self.get_type_of_visitor(cls):
                self._append_visit_function(cls)
            self.add_accept_method(cls)

        for cls in self.classes:
            for member in cls.members:
                self._convert_template_args(member)

        for cls in self.classes:
            for func in cls.functions:
                func.link()

        for cls in self.classes:
            self._generate_inline_functional(cls)

        for cls in self.classes:
            if cls.type == 'class' and cls.auto_generated:
                cls.add_get_type_function()

        for cls in self.classes:
            cls.on_linked(self)

    def validate_php_features(self):
        for cls in self.classes:
            for member in cls.members:
                if member.type == 'map':
                    key_type = member.template_args[0]
                    key_type = key_type if isinstance(key_type, str) else key_type.type
                    cls_type = self.find_class(key_type)
                    if cls_type is not None and cls_type.type != 'enum':
                        value_type = member.template_args[1] if isinstance(member.template_args[1], str) else member.template_args[1].type
                        Error.exit(Error.OBJECT_IS_KEY_OF_MAP, cls.name, key_type, value_type, member.name)
                if cls.type == 'enum' and member.initial_value is not None:
                    if '|' in member.initial_value or \
                       '&' in member.initial_value or \
                       '^' in member.initial_value or \
                       '~' in member.initial_value:
                        Error.exit(Error.ENUM_CANNOT_BE_COMBINATED, cls.name, member.name, member.initial_value)

    def _convert_template_args(self, member):
        args = []
        for arg in member.template_args:
            args.append(self._get_object_type(arg))
            if isinstance(args[-1], Object):
                self._convert_template_args(args[-1])
        member.template_args = args

    def _create_class(self, text, is_abstract):
        body, header, text = find_body(text)
        cls = Class()
        cls.parse(header)
        if is_abstract:
            cls.is_abstract = True

        if not self.is_side(cls.side):
            if cls.is_storage:
                self.classes_for_data.append(cls)
            return text
        if not self.generate_tests and cls.is_test:
            return text

        cls.parse_body(Parser(self.side, False, False, False), body)
        if self.find_class(cls.name):
            Error.exit(Error.DUBLICATE_CLASS, cls.name)
        for inner_cls in cls.inner_classes:
            self.classes.append(inner_cls)
        self.classes.append(cls)
        return text

    def is_serialised(self, cls):
        if cls.is_serialized:
            return True
        result = False
        for c in cls.superclasses:
            result = result or self.is_serialised(c)
        return result

    def is_visitor(self, cls):
        if cls.is_visitor:
            return True
        result = False
        for c in cls.superclasses:
            result = result or self.is_visitor(c)
        return result

    def is_function_override(self, cls, function):
        if cls.type == 'enum':
            return False
        if function.name in ['serialize', 'deserialize']:
            return len(cls.superclasses) > 0

        for c in cls.superclasses:
            for f in c.functions:
                if f.name == function.name and f.get_return_type().type == function.get_return_type().type and f.args == function.args:
                    return True
        is_override = False
        for c in cls.superclasses:
            is_override = is_override or self.is_function_override(c, function)
        return is_override

    def get_type_of_visitor(self, cls):
        if not cls.is_visitor:
            return None

        if cls.name.find('IVisitor') == 0:
            return cls.name

        for c in cls.superclasses:
            if not isinstance(c, Class):
                return 'IVisitor' + cls.name
            if c.is_visitor:
                return self.get_type_of_visitor(c)
        return 'IVisitor' + cls.name

    def _append_visit_function(self, cls):
        visitor_name = self.get_type_of_visitor(cls)
        visitor = self.find_class(visitor_name)
        append = cls.side == visitor.side and cls.side == self.side
        append = append or cls.side == 'both'
        if append:
            function = Function()
            function.name = 'visit'
            function.return_type = 'void'
            function.args.append(['ctx', cls.name + '*'])
            function.is_abstract = True
            visitor.functions.append(function)

            def comparator(func):
                return func.name
            visitor.functions.sort(key=comparator)

    def _get_object_type(self, type_name):
        cls = self.find_class(type_name)
        if cls:
            return cls
        obj = Object()
        type_name = obj.find_modifiers(type_name)
        obj.type = type_name
        obj.parse_type()
        obj.name = ""
        return obj

    def find_class(self, name):
        for cls in self.classes:
            if cls.name == name:
                return cls
        return None

    def _create_enum_class(self, text):
        body, header, text = find_body(text)
        cls = Class()
        cls.type = 'enum'
        cls.parse(header)
        if not self.is_side(cls.side):
            return text
        cls.parse_body(Parser(self.side, False, False, False), body)
        self.classes.append(cls)
        return text

    def create_visitor_class(self, cls):
        visitor_name = self.get_type_of_visitor(cls)
        visitor = self.find_class(visitor_name)
        if visitor is None:
            visitor = Class()
            visitor.name = visitor_name
            visitor.group = cls.group
            visitor.type = "class"
            visitor.is_abstract = True
            visitor.is_visitor = True
            visitor.is_virtual = True
            visitor.side = cls.side
            self.classes.append(visitor)

    def add_accept_method(self, cls):
        if not cls.is_visitor:
            return
        visitor = self.get_type_of_visitor(cls)
        if not visitor or visitor == cls.name:
            return
        function = Function()
        function.name = 'accept'
        function.return_type = Object.VOID
        function.args.append(['visitor', visitor + '*'])
        function.operations.append('visitor->visit(this);')
        function.link()
        cls.functions.append(function)

    def _create_declaration(self, text):
        lines = text.split("\n")
        line = lines[0]
        if len(lines) > 1:
            text = text[text.find("\n") + 1:]
        else:
            text = ""
        obj = Object()
        obj.parse(line)
        if not self.is_side(obj.side):
            return text
        self.objects.append(obj)
        return text

    def _create_function(self, text):
        body, header, text = find_body(text)
        function = Function()
        function.parse(header)
        if not self.is_side(function.side):
            return text
        function.parse_body(body)
        self.functions.append(function)
        return text

    def _generate_inline_functional(self, cls):
        if len(cls.superclasses) == 0:
            return
        for superclass in cls.superclasses:
            superclass = cls.superclasses[0]
            if not isinstance(superclass, Class):
                Error.exit(Error.INTERNAL_ERROR)
            self._generate_inline_functional(superclass)
            if not superclass.is_inline:
                continue
            for object in superclass.members:
                copy = deepcopy(object)
                cls.members.append(copy)
            for func in superclass.functions:
                copy = deepcopy(func)
                cls.functions.append(copy)

            superclass.subclasses.remove(cls)

        cls.superclasses = [i for i in cls.superclasses if not i.is_inline]

    def parse_serialize_protocol(self, path):
        buffer_ = open(self.configs_root + path).read()
        self._parse_serialize_protocol(buffer_)

    def load_default_serialize_protocol(self, language, serialize_format):
        buffer_ = protocols[language][serialize_format]
        if sys.version_info[0] == 3 and language == 'py':
            buffer_ = buffer_.replace('iteritems', 'items')
        self._parse_serialize_protocol(buffer_)
        pass

    def _parse_serialize_protocol(self, buffer):
        lines = buffer.split('\n')
        supported_types = []
        supported_types.extend(self.simple_types)
        supported_types.append('serialized')
        supported_types.append('pointer')
        supported_types.append('list<serialized>')
        supported_types.append('list<pointer>')
        supported_types.append('link')
        supported_types.append('list<link>')
        supported_types.append('serialized')
        supported_types.append('map')
        supported_types.append('enum')
        supported_types.append('list<enum>')
        for type_ in self.simple_types:
            list_type = "list<{0}>".format(type_)
            supported_types.append(list_type)

        serialize_protocol = list()
        serialize_protocol.append({})
        serialize_protocol.append({})
        for x in range(2):
            for type_ in supported_types:
                simple = type_ in self.simple_types
                p0 = self._load_protocol(lines, x, type_, True if simple else None, optional=type_ == 'list<enum>')
                p1 = p0 if not simple else self._load_protocol(lines, x, type_, False)
                serialize_protocol[x][type_] = []
                serialize_protocol[x][type_].extend([p0, p1])
        self.serialize_protocol = serialize_protocol

    def _load_protocol(self, lines, serialize_type, type, initial_value=None, optional=False):
        stypes = ['serialize', 'deserialize']
        sinit = ['with default value', 'without default value']
        in_type = False
        in_serialize = False
        in_initial_value = initial_value is None
        pattern = []
        for oline in lines:
            if oline.endswith('\n'):
                oline = oline[0:-1]
            line = oline.strip()
            if not line:
                continue
            if not in_type and line.startswith('#'):
                types = line[1:].split(',')
                for type_ in types:
                    in_type = in_type or (type == type_.strip())
                continue
            if in_type and line.startswith('#' + stypes[serialize_type]):
                in_serialize = True
                continue
            if in_type and in_serialize and not in_initial_value and line.startswith('#' + sinit[0 if initial_value else 1]):
                in_initial_value = True
                continue
            if in_type and in_serialize and in_initial_value:
                if line.startswith('#'):
                    break
                pattern.append(oline)
        def_ = pattern
        pattern = '\n'.join(pattern)
        # standard serialize
        pattern = pattern.replace('{', '__begin__')
        pattern = pattern.replace('}', '__end__')
        pattern = pattern.replace('$(FIELD)', '{0}')
        pattern = pattern.replace('$(TYPE)', '{1}')
        pattern = pattern.replace('$(DEFAULT_VALUE)', '{2}')
        pattern = pattern.replace('$(OWNER)', '{4}')
        pattern = pattern.replace('$(ARG_0)', '{5}')
        pattern = pattern.replace('$(ARG_1)', '{6}')
        # for map<key, value>
        pattern = pattern.replace('$(KEY_SERIALIZE)', '{1}')
        pattern = pattern.replace('$(VALUE_SERIALIZE)', '{2}')
        pattern = pattern.replace('$(KEY)', '{3}')
        pattern = pattern.replace('$(VALUE_TYPE)', '{4}')
        pattern = pattern.replace('$(VALUE)', '{5}')
        # for python:
        pattern = pattern.replace('$(__begin____end__)', '{3}')

        if not pattern and not optional:
            print('cannot find pattern for args:')
            print(type, stypes[serialize_type], initial_value)
            print('in_type', in_type)
            print('in_serialize', in_serialize)
            print('in_initial_value', in_initial_value)
            print(def_)
            exit(-1)
        return pattern
