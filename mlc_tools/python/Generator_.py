from ..language.Generator_ import *
from ..Object import *
from ..Function import Function


class Generator(GeneratorBase):

    def __init__(self):
        GeneratorBase.__init__(self)

    def generate_data_storage(self, parser):
        storage = DataStoragePython('DataStorage', parser.classes, parser)
        parser.classes.append(storage)

    def generate_factory(self, parser, writer):
        from .constants import FACTORY

        line = '''
        if type == "{0}":
            from . import {0}
            return {0}.{0}()'''
        builders = ''
        for cls in parser.classes:
            builders += line.format(cls.name)
        content = FACTORY.format(builders=builders)
        writer.save_file('Factory.py', content)

    def generate_init_files(self, parser, writer):
        writer.save_file('__init__.py', '')
        
    @staticmethod
    def generate_visitors_pattern(parser):
        generator = VisitorPatternGenerator()
        generator.generate(parser)


class DataStoragePython(DataStorage):

    def __init__(self, *args):
        DataStorage.__init__(self, *args)

    def create_shared_method(self):
        obj = Object()
        obj.type = self.name
        obj.name = '__instance'
        obj.is_static = True
        obj.is_pointer = True
        obj.access = AccessSpecifier.private
        self.members.append(obj)

        method = Function()
        method.name = 'shared'
        method.args.append(['', ''])
        method.return_type = self.name
        method.is_static = True
        method.translated = True
        method.operations.append('        if not {}.__instance:'.format(self.name))
        method.operations.append('    {0}.__instance = {0}()'.format(self.name))
        method.operations.append('return {}.__instance'.format(self.name))
        self.functions.append(method)

    def create_getters(self, classes):
        for class_ in classes:
            if class_.is_storage and (class_.side == self.parser.side or class_.side == 'both'):
                map_name = get_data_list_name(get_data_name(class_.name))
                method = Function()
                method.name = 'get' + class_.name
                method.args.append(['name', ''])
                method.operations.append('        if not self._loaded and name not in self.{}:'.format(map_name))
                method.operations.append('    from .{0} import {0}'.format(class_.name))
                method.operations.append('    self.{}[name] = {}()'.format(map_name, class_.name))
                method.operations.append('    self.{}[name].name = name'.format(map_name))
                method.operations.append('return self.{}[name]'.format(map_name))
                method.translated = True
                self.functions.append(method)

    def add_initialize_function_json(self):
        method = Function()
        method.name = 'initialize_json'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('        js = json.loads(content)')
        method.operations.append('self.deserialize_json(js)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)

    def add_initialize_function_xml(self):
        method = Function()
        method.name = 'initialize_xml'
        method.return_type = 'void'
        method.is_const = True
        method.args.append(['content', 'string'])
        method.translated = True

        method.operations.append('        root = ET.fromstring(content)')
        method.operations.append('self.deserialize_xml(root)')
        method.operations.append('self._loaded = True')
        self.functions.append(method)


class VisitorPatternGenerator:
    def __init__(self):
        self.parser = None
        self.base_visitor_classes = {}

    def generate(self, parser):
        self.parser = parser

        # find visitor and bases classes
        for cls in parser.classes:
            base_class_name = self.get_base_visitor_name(cls)
            if base_class_name is None:
                continue
            if base_class_name not in self.base_visitor_classes:
                self.base_visitor_classes[base_class_name] = []
            self.base_visitor_classes[base_class_name].append(cls)

        # generate acceptors interface, visit methods
        for base_class_name in self.base_visitor_classes:
            visitors = self.base_visitor_classes[base_class_name]
            self.generate_acceptor_interface(base_class_name, visitors)
            for visitor in visitors:
                self.add_accept_method(visitor, base_class_name)

    def get_base_visitor_name(self, cls):
        for superclass_name in cls.superclasses:
            if superclass_name in self.base_visitor_classes:
                return superclass_name

            superclass = self.parser.find_class(superclass_name)
            if not superclass:
                # TODO: remove print
                if superclass_name.startswith('IVisitor'):
                    # Correct situation. The class can be inherited from the IVisitor interface
                    continue
                Error.exit(Error.UNKNOWN_SUPERCLASS, cls.name, superclass_name)
            if superclass.is_visitor:
                return superclass_name
        return None

    def generate_acceptor_interface(self, base_class_name, visitors):
        assert (len(visitors) > 0)
        acceptor = Class()
        acceptor.name = 'IVisitor' + base_class_name
        acceptor.group = visitors[0].group
        acceptor.type = "class"
        acceptor.is_abstract = True
        acceptor.is_virtual = True
        acceptor.side = visitors[0].side
        self.parser.classes.append(acceptor)

        for visitor in visitors:
            method = Function()
            method.name = 'visit_' + visitor.name[0].lower() + visitor.name[1:]
            method.return_type = 'void'
            method.args.append(['ctx', visitor.name + '*'])
            method.is_abstract = True
            acceptor.functions.append(method)

        method = Function()
        acceptor.functions.append(method)
        method.name = 'visit'
        method.return_type = 'void'
        method.args.append(['ctx', base_class_name + '*'])
        method.operations.append('''
            if(!ctx)
            {
                return;
            }''')
        for visitor in visitors:
            method.operations.append('''
            else if(ctx.__class__ == {})
            {{
                this->visit_{}(ctx)
            }}'''.format(visitor.name, visitor.name[0].lower() + visitor.name[1:]))




        def comparator(func):
            return func.args[0][1]

        acceptor.functions.sort(key=comparator)

    @staticmethod
    def add_accept_method(cls, base_class_name):
        method = Function()
        method.name = 'accept'
        method.return_type = Objects.VOID
        method.args.append(['visitor', base_class_name + '*'])
        method.operations.append('visitor->visit(this);')
        cls.functions.append(method)
