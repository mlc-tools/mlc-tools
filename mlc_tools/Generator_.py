from TestClass import GeneratorTestInterfaces
from .Function import Function
from .Object import *
from .Class import Class
from .Error import Error


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
        
        pass
    
    def generate_acceptor_interfaces(self, parser):
        self.parser = parser

        # find visitor and bases classes
        self.base_visitor_classes = {}
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
            function = Function()
            function.name = 'visit'
            function.return_type = 'void'
            function.args.append(['ctx', visitor.name + '*'])
            function.is_abstract = True
            acceptor.functions.append(function)
    
        def comparator(func):
            return func.args[0][1]
    
        acceptor.functions.sort(key=comparator)
    
    @staticmethod
    def add_accept_method(cls, base_class_name):
        function = Function()
        function.name = 'accept'
        function.return_type = Objects.VOID
        function.args.append(['visitor', base_class_name + '*'])
        function.operations.append('visitor->visit(this);')
        cls.functions.append(function)
