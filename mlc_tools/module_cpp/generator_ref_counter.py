from mlc_tools.base.model import Model
from mlc_tools.core.class_ import Class
from mlc_tools.core.function import Function
from mlc_tools.core.object import Object, Objects, AccessSpecifier


RETAIN_INT = '++this->_reference_counter;'
RETAIN_ATOMIC = '_reference_counter.fetch_add(1, std::memory_order_relaxed);'
RELEASE_INT = '''
--this->_reference_counter;
auto counter = this->_reference_counter;
if(counter == 0)
{
    delete this;
}
return counter;
'''
RELEASE_ATOMIC = '''
auto ret = _reference_counter.fetch_sub(1, std::memory_order_acq_rel);
if(ret == 1)
{
    delete this;
}
return ret;
'''


class GeneratorRefCounter(object):
    def __init__(self):
        self.prefer_type = 'int'
        self.retain = RETAIN_INT
        self.release = RELEASE_INT

    def generate(self, model: Model):
        if not model.generate_ref_counter:
            return

        if model.side == 'server':
            self.prefer_type = 'std::atomic<int>'
            self.retain = RETAIN_ATOMIC
            self.release = RELEASE_ATOMIC

        for cls in model.classes:
            if not cls.superclasses and cls.type != 'enum' and not cls.is_abstract:
                self._add(cls)

    def _add(self, cls: Class):
        if not cls.has_member_with_name('_reference_counter'):
            ref_counter = Object()
            ref_counter.name = '_reference_counter'
            ref_counter.type = self.prefer_type
            ref_counter.initial_value = '1'
            ref_counter.is_runtime = True
            ref_counter.access = AccessSpecifier.private
            cls.members.append(ref_counter)
        if not cls.has_method_with_name('retain'):
            retain = Function()
            retain.name = 'retain'
            retain.return_type = Objects.VOID
            retain.operations.extend(self.retain.split('\n'))
            cls.functions.append(retain)
        if not cls.has_method_with_name('release'):
            release = Function()
            release.name = 'release'
            release.return_type = Objects.INT
            release.operations.extend(self.release.split('\n'))
            cls.functions.append(release)
