from ..core.class_ import Class


PREDEFINED = '''
class @{name}
{
    constructor()
    {
        this.listeners = [];
        this.objects = [];
    }

    add(object, callback)
    {
        this.objects.push(object);
        this.listeners.push(callback);
    }
    remove(object)
    {
        let index = this.objects.indexOf(object);
        if(index != -1)
        {
            this.listeners.splice(index, 1);
            this.objects.splice(index, 1);
        }
    }
    notify()
    {
        for (let index in this.listeners)
        {
            let object = this.objects[index];
            let callback = this.listeners[index];
            callback.apply(object, arguments);
        }
    }
}

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
        filename = GeneratorObserver.get_observable_name() + '.js'
        text = text.replace('@{name}', GeneratorObserver.get_observable_name())

        mock = GeneratorObserver.get_mock()
        model.add_file(mock, filename, text)
        model.add_class(mock)
