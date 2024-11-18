import re
import sys
from ..base.model import Model
from ..core.object import Object
from ..core.class_ import Class
from ..core.function import Function
from ..utils.error import Error
from ..utils.common import parse_object, smart_split


class Parser(object):

    def __init__(self, model):
        self.model = model

    def parse_files(self, files):
        for path in files:
            text = open(path, encoding='utf-8').read()
            self.parse_text(text)

    def parse_text(self, text):
        text = self.remove_comments(text)
        while text:
            if Parser._is_class(text):
                text = self._create_class(text, False)
            elif Parser._is_interface(text):
                text = self._create_class(text, True)
            elif Parser._is_enum(text):
                text = self._create_enum_class(text)
            elif Parser._is_include(text):
                text = self._create_include(text)
            elif Parser._is_function(text):
                text = self._create_function(text)
            elif Parser._is_constructor(text):
                text = self._create_constructor(text)
            else:
                text = self._create_member(text)
            text = text.strip()

    @staticmethod
    def remove_comments(text):
        left = text.find('/*')
        while left > -1:
            right = text.find('*/', left)
            if right > -1:
                text = text[:left] + text[right + 2:]
            left = text.find('/*')
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if '//' in line:
                lines[i] = line[0:line.find('//')]
        text = '\n'.join(lines).strip()
        return text

    def check_skip(self, line):
        corresponds = True
        first_match = True
        for lang in ['cpp', 'py', 'php', 'js']:
            modifier = ':' + lang
            if modifier in line:
                if first_match:
                    first_match = False
                    corresponds = False
                corresponds = corresponds or self.model.is_lang(lang)
                line = line.replace(modifier, '')
        return not corresponds, line

    def _create_class(self, text, is_abstract):
        body, header, text = Parser.parse_body(text)
        skip, header = self.check_skip(header)
        cls = Class()
        Parser.parse_class(cls, header)
        if is_abstract:
            cls.is_abstract = True

        skip = skip or not self.model.is_side(cls.side)
        if skip:
            if cls.is_storage:
                self.model.classes_for_data.append(cls)
            return text

        parser = Parser(self.model.empty_copy())
        parser.model.side = self.model.side
        parser.parse_class_body(cls, body)
        if self.model.has_class(cls.name):
            Error.exit(Error.DUBLICATE_CLASS, cls.name)
        for inner_cls in cls.inner_classes:
            self.model.add_class(inner_cls)

        cls.generate_constructor()
        self.model.add_class(cls)
        return text

    def _create_enum_class(self, text):
        body, header, text = Parser.parse_body(text)

        skip, header = self.check_skip(header)
        if skip:
            return text

        cls = Class()
        cls.type = 'enum'
        Parser.parse_class(cls, header)
        cls.superclasses.append('BaseEnum')
        if not self.model.is_side(cls.side):
            return text
        parser = Parser(self.model.empty_copy())
        parser.model.side = self.model.side
        parser.parse_class_body(cls, body)
        self.model.add_class(cls)
        return text

    def _create_member(self, text):
        lines = text.split('\n')
        line = lines[0]
        if len(lines) > 1:
            text = text[text.find('\n') + 1:]
        else:
            text = ''

        skip, line = self.check_skip(line)
        if skip:
            return text

        obj = Object()
        self.parse_object(obj, line)
        if self.model.is_side(obj.side):
            self.model.objects.append(obj)
        return text

    def _create_include(self, text):
        k = text.find('\n')
        line = text[0:k]
        text = text[k+1:]
        class_name = line.replace('@include ', '').strip()
        self.model.includes.add(class_name)
        return text

    def _create_function(self, text):
        body, header, text = Parser.parse_body(text)
        skip, header = self.check_skip(header)
        if skip:
            return text
        method = Function()
        self.parse_function_header(method, header)
        if self.model.is_side(method.side):
            method.parse_method_body(body)
            self.model.functions.append(method)
        return text

    def _create_constructor(self, text):
        body, header, text = Parser.parse_body(text)
        skip, header = self.check_skip(header)
        if skip:
            return text
        constructor = Function()
        self.parse_function_header(constructor, 'function void {}'.format(header))
        if self.model.is_side(constructor.side):
            constructor.parse_method_body(body)
            self.model.functions.append(constructor)
        return text

    @staticmethod
    def create_object(description):
        parser = Parser(Model())
        parser.parse_text(description)
        return parser.model.objects[0]

    @staticmethod
    def create_function(description):
        parser = Parser(Model())
        parser.parse_text(description)
        return parser.model.functions[0]

    def parse_object(self, obj, line):
        if ';' in line:
            Error.warning(Error.WARNING_SYNTAX, line)
            line = line.replace(';', '')

        # parse initialize value
        expression = ''
        k = line.find('=')
        if k > -1:
            expression = line[k + 1:].strip()
            line = line[0:k].strip()
        if expression:
            obj.initial_value = expression

        # parse type, name, template arguments
        parse_object(obj, line)

        has_callable, obj.callable_args, obj.type = self.parse_function_args(obj.type)
        obj.callable_args = [a[1] for a in obj.callable_args]
        if not has_callable:
            obj.callable_args = None

        # parse specific modifiers
        obj.type = obj.find_modifiers(obj.type)
        obj.is_pointer = obj.check_pointer()
        obj.is_ref = obj.check_ref()
        if not self.model.is_side(obj.side):
            return

        # recursive parsing template arguments
        args = []
        for arg_desc in obj.template_args:  # type: str
            arg = Object()
            self.parse_object(arg, arg_desc)
            args.append(arg)
        obj.template_args = args

    FUNC_0 = re.compile(r'function<([\w, ]+?)>')
    FUNC_1 = re.compile(r'function<[\w, ]+?>')
    FUNC_0s = re.compile(r'fn<([\w, ]+?)>')
    FUNC_1s = re.compile(r'fn<[\w, ]+?>')
    FUNC_2 = re.compile(r'{.*}')

    def parse_function_header(self, method, line):
        line = line.strip()

        use_s = False
        templates = Parser.FUNC_0.findall(line)
        if not templates:
            templates = Parser.FUNC_0s.findall(line)
            use_s = True
        if templates:
            line = Parser.FUNC_1.sub('', line) if not use_s else Parser.FUNC_1s.sub('', line)
            method.template_types = smart_split(templates[0], ',')
            method.template_types = [x.strip() for x in method.template_types]
        else:
            len_function = 8 if line.startswith('function') else 2 # len('function') or len('fn')
            line = line[len_function:].strip()

        has_callable, method.args, line = self.parse_function_args(line)
        assert has_callable

        line = line.replace(';', '')
        line = Parser.FUNC_2.sub('', line)
        k = line.rfind(' ')

        name_s = line[k:].strip()
        name_s = method.find_modifiers(name_s)
        method.name = name_s

        return_s = line[:k].strip()
        method.return_type = Object()
        self.parse_object(method.return_type, return_s)
        return method

    def parse_function_args(self, line):
        result = []
        left = line.find('(')
        last = line.rfind(')')
        if left == -1 or last == -1 or last < left:
            return False, result, line

        args_s = line[left + 1:last]
        args = smart_split(args_s, ',')

        for arg in args:
            arg = arg.strip()
            if arg.startswith('const '):
                Error.exit(Error.ERROR_CONST_MODIFIER, arg)

            obj = Object()
            self.parse_object(obj, arg)
            result.append([obj.name, obj])

        line = line[:left] + line[last + 1:]
        return True, result, line

    @staticmethod
    def _is_class(line):
        return line.find('class') == 0

    @staticmethod
    def _is_interface(line):
        return line.find('interface') == 0

    @staticmethod
    def _is_function(line):
        return line.find('function') == 0 or line.find('fn') == 0

    @staticmethod
    def _is_constructor(line):
        return line.find('constructor') == 0

    @staticmethod
    def _is_include(line):
        return line.startswith('@include')

    @staticmethod
    def _is_enum(line):
        return line.find('enum') == 0

    @staticmethod
    def parse_body(text):
        text = text.strip()
        body = ''
        k = text.find('\n')
        if k > -1:
            header = text[0:k]
        else:
            header = text
        if header.find(':external') == -1 and header.find(':abstract') == -1:
            text = text[text.find('{'):]
            counter = 0
            left = 0
            last = 0
            for char in text:
                last += 1
                if not counter and char == '{':
                    counter += 1
                    left = last
                    continue

                if char == '{':
                    counter += 1
                if char == '}':
                    counter -= 1
                if not counter:
                    body = text[left:last-1]
                    text = text[last:]
                    break
        else:
            text = text[len(header):].strip()
        return body, header, text

    def load_default_serialize_protocol(self, text):
        lines = text.split('\n')
        supported_types = []
        supported_types.extend(self.model.simple_types)
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
        for type_ in self.model.simple_types:
            list_type = "list<{0}>".format(type_)
            supported_types.append(list_type)

        serialize_protocol = list()
        serialize_protocol.append({})
        serialize_protocol.append({})
        for index in range(2):
            for type_ in supported_types:
                simple = type_ in self.model.simple_types
                protocol_0 = self._load_protocol(lines, index, type_, True if simple else None,
                                                 optional=type_ == 'list<enum>')
                protocol_1 = protocol_0 if not simple else self._load_protocol(lines, index, type_, False)
                serialize_protocol[index][type_] = []
                serialize_protocol[index][type_].extend([protocol_0, protocol_1])
        self.model.serialize_protocol = serialize_protocol

    @staticmethod
    def _load_protocol(lines, serialize_type, type_object, initial_value=None, optional=False):
        serialize_types = ['serialize', 'deserialize']
        serialize_init = ['with default value', 'without default value']
        in_type = False
        in_serialize = False
        in_initial_value = initial_value is None
        pattern = []
        if type_object in ['int64_t', 'uint', 'uint64_t', 'unsigned']:
            type_object = 'int'
        if type_object in ['double']:
            type_object = 'float'
        if type_object in ['list<int64_t>', 'list<uint>', 'list<uint64_t>', 'list<unsigned>']:
            type_object = 'list<int>'
        if type_object in ['list<double>']:
            type_object = 'list<float>'
        for original_line in lines:
            if original_line.endswith('\n'):
                original_line = original_line[0:-1]
            line = original_line.strip()
            if not line:
                continue
            if not in_type and line.startswith('#'):
                types = line[1:].split(',')
                for type_ in types:
                    in_type = in_type or (type_object == type_.strip())
                continue
            if in_type and line.startswith('#' + serialize_types[serialize_type]):
                in_serialize = True
                continue
            if in_type and in_serialize and not in_initial_value and \
                    line.startswith('#' + serialize_init[0 if initial_value else 1]):
                in_initial_value = True
                continue
            if in_type and in_serialize and in_initial_value:
                if line.startswith('#'):
                    break
                pattern.append(original_line)
        def_ = pattern
        pattern = '\n'.join(pattern)
        # standard serialize
        pattern = pattern.replace('{', '{{')
        pattern = pattern.replace('}', '}}')
        pattern = pattern.replace('$(FIELD)', '{field}')
        pattern = pattern.replace('$(TYPE)', '{type}')
        pattern = pattern.replace('$(DEFAULT_VALUE)', '{default_value}')
        pattern = pattern.replace('$(OWNER)', '{owner}')
        pattern = pattern.replace('$(ARG_0)', '{arg_0}')
        pattern = pattern.replace('$(ARG_1)', '{arg_1}')
        pattern = pattern.replace('$(FORMAT)', '{format}')
        pattern = pattern.replace('$(NAMESPACE)', '{namespace}')
        # for map<key, value>
        pattern = pattern.replace('$(KEY_SERIALIZE)', '{key_serialize}')
        pattern = pattern.replace('$(VALUE_SERIALIZE)', '{value_serialize}')
        pattern = pattern.replace('$(KEY)', '{key}')
        pattern = pattern.replace('$(VALUE_TYPE)', '{value_type}')
        pattern = pattern.replace('$(VALUE)', '{value}')
        # for module_python:
        pattern = pattern.replace('$({{}})', '{{}}')

        if not pattern and not optional:
            print('cannot find pattern for args:')
            print(type_object, serialize_types[serialize_type], initial_value)
            print('in_type', in_type)
            print('in_serialize', in_serialize)
            print('in_initial_value', in_initial_value)
            print(def_)
            sys.exit(-1)
        return pattern

    @staticmethod
    def parse_class(cls: Class, line: str):
        from ..utils.common import smart_split
        line = line.strip()
        if cls.type in line:
            line = line[len(cls.type):]
        elif 'interface' in line:
            line = line[len('interface'):]
        line = cls.find_modifiers(line)

        pattern = re.compile(r' ([\w/]+)(<(\w+)>)*')
        parts = pattern.findall(line)[0]
        cls.name = parts[0]
        cls.superclasses = smart_split(parts[2], ',')
        cls.template_args = []
        if '/' in cls.name:
            k = cls.name.rindex('/')
            cls.group = cls.name[0:k]
            cls.name = cls.name[k + 1:]

    def parse_class_body(self, cls: Class, body: str):
        self.parse_text(body)

        for member in self.model.objects:
            if self.model.has_class(member.type):
                member.type = cls.name + member.type
            for i, arg in enumerate(member.template_args):
                if self.model.has_class(arg):
                    member.template_args[i] = cls.name + member.template_args[i]

        for func in self.model.functions:
            if self.model.has_class(func.return_type):
                func.return_type = cls.name + func.return_type
            for arg in func.args:
                if self.model.has_class(arg[1]):
                    arg[1] = cls.name + arg[1]

            for inner_class in self.model.classes:
                pattern = re.compile(r'\b{}\b'.format(inner_class.name))
                new_name = cls.name + inner_class.name
                for i, line in enumerate(func.operations):
                    func.operations[i] = re.sub(pattern, new_name, line)
        for inner_class in self.model.classes:
            inner_class_name = inner_class.name
            inner_class.name = cls.name + inner_class.name
            inner_class.group = cls.group
            inner_class.side = cls.side
            inner_class.is_test = cls.is_test
            cls.inner_classes.append(inner_class)

            for obj in self.model.objects:
                if obj.type == inner_class_name:
                    obj.type = inner_class.name
                for arg in obj.template_args:
                    if arg.type == inner_class_name:
                        arg.type = inner_class.name

            for method in self.model.functions:
                for _, arg in method.args:
                    if arg.type == inner_class_name:
                        arg.type = inner_class.name
                if method.return_type.type == inner_class_name:
                    method.return_type.type = inner_class.name

        cls.members = self.model.objects
        cls.functions = self.model.functions
        cls.user_includes = self.model.includes
        self.model.includes = set()

        for member in cls.members:
            member.set_default_initial_value()