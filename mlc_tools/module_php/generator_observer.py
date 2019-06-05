from ..core.class_ import Class


PREDEFINED = '''<?php
class Observable{
    private $listeners = array();
    private $objects = array();

    public function add($object, $callback) {
        array_push($this->listeners, $callback);
        array_push($this->objects, $object);
    }
    public function remove($object) {
        $index = array_search($object, $this->objects);
        if($index !== false) {
            array_splice($this->listeners, $index, 1);
            array_splice($this->objects, $index, 1);
        }
    }
    public function notify(...$arg){
        for ($i = 0; $i < count($this->listeners); ++$i) {
            $func = $this->listeners[$i];
            $obj = $this->objects[$i];
            $obj->$func(...$arg);
        }
    }
};
?>
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
        filename = GeneratorObserver.get_observable_name() + '.php'
        text = text.replace('@{namespace}', 'mg')
        text = text.replace('@{name}', GeneratorObserver.get_observable_name())
        model.add_file(None, filename, text)

        model.add_class(GeneratorObserver.get_mock())
