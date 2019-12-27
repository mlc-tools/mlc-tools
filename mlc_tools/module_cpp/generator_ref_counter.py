from mlc_tools.core.function import Function
from mlc_tools.core.object import Object, Objects, AccessSpecifier


class GeneratorRefCounter(object):

    def __init__(self):
        pass

    def generate(self, model):
        self.model = model
        for cls in model.classes:
            if not cls.superclasses and cls.type != 'enum':
                self._add(cls)

    def _add(self, cls):
        retain = Function()
        retain.name = 'retain'
        retain.return_type = Objects.VOID
        retain.operations.append('this->_reference_counter += 1;')

        release = Function()
        release.name = 'release'
        release.return_type = Objects.INT
        release.operations.append('this->_reference_counter -= 1;')
        release.operations.append('auto counter = this->_reference_counter;')
        release.operations.append('if(counter == 0)')
        release.operations.append('delete this;')
        release.operations.append('return counter;')

        ref_counter = Object()
        ref_counter.name = '_reference_counter'
        ref_counter.type = 'int'
        ref_counter.initial_value = '1'
        ref_counter.is_runtime = True
        ref_counter.access = AccessSpecifier.private

        cls.members.append(ref_counter)
        cls.functions.append(retain)
        cls.functions.append(release)
