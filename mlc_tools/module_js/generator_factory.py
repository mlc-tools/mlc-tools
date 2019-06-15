
from .writer import Writer


class GeneratorFactory(object):

    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        writer = Writer('')
        writer.model = model
        content = writer.prepare_file(FACTORY)
        model.add_file(None, 'Factory.js', content)


FACTORY = '''
class Factory
{
}

Factory.build = function (type)
{
    return eval("new " + type + "()");
};
Factory.create_command_from_json = function (payload)
{
    let json = JSON.parse(payload);
    for(let key in json)
    {
        let command = Factory.build(key);
        if(command)
        {
            command.deserialize_json(json[key]);
        }
        return command;
    }
};

Factory.serialize_command_to_json = function (command)
{
    let json = {};
    json[command.get_type()] = {};
    command.serialize_json(json[command.get_type()]);
    return JSON.stringify(json);
};

Factory.clone_object = function (obj)
{
    let payload = Factory.serialize_command_to_json(obj);
    return Factory.create_command_from_json(payload);
};
'''
