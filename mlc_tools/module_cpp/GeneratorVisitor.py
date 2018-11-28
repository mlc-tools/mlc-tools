from ..core.Object import *
from ..core.Class import Class
from ..core.Function import Function
from ..base.Parser import Parser
from ..utils.Error import Error


class GeneratorVisitor:

    def __init__(self):
        self.model = None
        self.base_visitor_classes = {}

    def generate(self, model):
        self.model = model

        # find visitor and bases classes
        for cls in model.classes:
            base_class_name = self.get_base_visitor_name(cls)
            if base_class_name is None:
                continue
            if base_class_name not in self.base_visitor_classes:
                self.base_visitor_classes[base_class_name] = []
                base_class = model.get_class(base_class_name)
                self.base_visitor_classes[base_class_name].append(base_class)
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

            superclass = self.model.get_class(superclass_name)
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
        acceptor.superclasses.append('SerializedObject')
        self.model.classes.append(acceptor)

        for visitor in visitors:
            method = Function()
            method.name = 'visit'
            method.return_type = Objects.VOID
            method.args.append(['ctx', Parser.create_object(visitor.name + '*')])
            method.args[0][1].denied_intrusive = True
            method.is_abstract = True
            acceptor.functions.append(method)

        def comparator(func):
            return func.args[0][1]
        acceptor.functions.sort(key=comparator)

    @staticmethod
    def add_accept_method(cls, base_class_name):
        method = Function()
        method.name = 'accept'
        method.return_type = Objects.VOID
        method.args.append(['visitor', Parser.create_object('IVisitor' + base_class_name + '*')])
        method.operations.append('visitor->visit(this);')
        cls.functions.append(method)
