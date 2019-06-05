from ..core.class_ import Class


PREDEFINED = '''
class @{name}:

    def __init__(self):
        self._listeners = {}
        self._add = {}
        self._remove = []
        self._locked = 0

    def _is_locked(self):
        return self._locked != 0

    def _lock(self):
        self._locked += 1

    def _unlock(self):
        self._locked -= 1
        if not self._is_locked():
            for object in self._add:
                self._listeners[object] = self._add[object]
            for object in self._remove:
                del self._listeners[object]
            self._add = {}
            self._remove = []

    def _call(self, obj, func, *args):
        def isclass(obj_):
            return isinstance(obj_, object)

        if isclass(obj):
            func(obj, *args)
        else:
            func(*args)

    def add(self, object, functor):
        if self._is_locked():
            if object in self._remove:
                self._remove.remove(object)
            else:
                self._add[object] = functor
        else:
            self._listeners[object] = functor

    def remove(self, object):
        if self._is_locked():
            self._remove.append(object)
        else:
            del self._listeners[object]

    def notify(self, *args):
        self._lock()
        for object in self._listeners:
            if object not in self._remove:
                self._call(object, self._listeners[object], *args)
        self._unlock()
'''


class GeneratorObserver(object):

    def __init__(self):
        pass

    @staticmethod
    def get_mock():
        cls = Class()
        cls.name = GeneratorObserver.get_observable_name()
        cls.type = 'class'
        cls.auto_generated = False
        return cls

    @staticmethod
    def get_observable_name():
        return 'Observable'

    @staticmethod
    def generate(model):
        text = PREDEFINED
        filename = GeneratorObserver.get_observable_name() + '.py'
        text = text.replace('@{namespace}', 'mg')
        text = text.replace('@{name}', GeneratorObserver.get_observable_name())
        model.add_file(None, filename, text)

        model.add_class(GeneratorObserver.get_mock())
