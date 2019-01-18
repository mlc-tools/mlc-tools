from .parser import Parser
from ..core.object import Objects
from ..core.class_ import Class
from ..core.function import Function
from ..utils.error import Error


class GeneratorVisitor(object):

    def __init__(self):
        self.model = None
        self.base_visitor_classes = {}
        self.acceptors_interfaces = []
        self.support_override_methods = False

    def generate(self, model, support_override_methods):
        self.model = model
        self.support_override_methods = support_override_methods

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

        if not self.support_override_methods:
            # change name of methods to classes extends IVisitor interfaces
            for cls in model.classes:
                superclass_name = cls.superclasses[0] if cls.superclasses else None
                while superclass_name is not None:
                    if superclass_name in self.acceptors_interfaces:
                        self.override_methods(cls)
                        break
                    superclass = model.get_class(superclass_name)
                    superclass_name = superclass.superclasses[0] if superclass.superclasses else None

    def get_base_visitor_name(self, cls):
        for superclass_name in cls.superclasses:
            if superclass_name in self.base_visitor_classes:
                return superclass_name

            if not self.model.has_class(superclass_name):
                if superclass_name.startswith('IVisitor'):
                    # Correct situation. The class can be inherited from the IVisitor interface
                    continue
                Error.exit(Error.UNKNOWN_SUPERCLASS, cls.name, superclass_name)

            superclass = self.model.get_class(superclass_name)
            if superclass.is_visitor:
                return superclass_name

            result = self.get_base_visitor_name(superclass)
            if result:
                return result
        return None

    def generate_acceptor_interface(self, base_class_name, visitors):
        assert visitors
        acceptor = Class()
        acceptor.name = 'IVisitor' + base_class_name
        acceptor.group = visitors[0].group
        acceptor.type = "class"
        acceptor.is_abstract = True
        acceptor.is_virtual = True
        acceptor.side = visitors[0].side
        self.model.add_class(acceptor)
        self.acceptors_interfaces.append(acceptor.name)

        for visitor in visitors:
            method = Function()
            if self.support_override_methods:
                method.name = 'visit'
            else:
                method.name = 'visit_' + visitor.name[0].lower() + visitor.name[1:]
            method.return_type = Objects.VOID
            method.args.append(['ctx', Parser.create_object(visitor.name + '*')])
            method.is_abstract = True
            method.args[0][1].denied_intrusive = True
            acceptor.functions.append(method)

        if not self.support_override_methods:
            method = Function()
            acceptor.functions.append(method)
            method.name = 'visit'
            method.return_type = Objects.VOID
            method.args.append(['ctx', Parser.create_object(base_class_name + '*')])
            method.operations.append('''
                if(!ctx)
                {
                    return;
                }''')
            for visitor in visitors:
                method.operations.append('''
                else if(ctx->get_type() == {}::TYPE)
                {{
                    this->visit_{}(ctx);
                }}'''.format(visitor.name, visitor.name[0].lower() + visitor.name[1:]))

        def comparator(func):
            return func.args[0][1].type
        acceptor.functions.sort(key=comparator)

    @staticmethod
    def add_accept_method(class_, base_class_name):
        method = Function()
        method.name = 'accept'
        method.return_type = Objects.VOID
        method.args.append(['visitor', Parser.create_object('IVisitor' + base_class_name + '*')])
        method.operations.append('visitor->visit(this);')
        class_.functions.append(method)

    @staticmethod
    def override_methods(class_):
        for method in class_.functions:
            if method.name == 'visit' and len(method.args) == 1:
                arg_type = method.args[0][1].type
                method.name = 'visit_%s' % (arg_type[0].lower()) + arg_type[1:]
