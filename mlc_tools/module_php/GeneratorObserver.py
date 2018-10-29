from mlc_tools.core.Class import Class


PREDEFINED = '''<?php
class Observable{
    private $listeners = array();
    private $objects = array();

    public function add($object, $callback){
        array_push($this->listeners, $callback);
        array_push($this->objects, $object);
    }
    public function remove($object){
        $index = array_search($object, $this->objects);
        if($index !== false){
            unset($this->listeners[$index]);
            unset($this->objects[$index]);
        }
    }
    public function notify(...$arg){
        foreach($this->listeners as $listener){
            $listener(...$arg);
        }
    }
};
?>
'''


class GeneratorObserver:
    
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
    
    def generate(self, writer):
        text = PREDEFINED
        filename = GeneratorObserver.get_observable_name() + '.php'
        text = text.replace('@{namespace}', 'mg')
        text = text.replace('@{name}', GeneratorObserver.get_observable_name())
        writer.save_file(filename, text)