
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

// TODO: move to generator
length_of = function (obj)
{
    let result = obj.length;
    return result;
};

compare = function (lhs, rhs)
{
    if(lhs == undefined || rhs == undefined)
    {
        return lhs == rhs;
    }
    let l = lhs.valueOf();
    let r = rhs.valueOf();
    return l == r;
};

class Factory
{
}

Factory.build = function (type)
{
    return eval("new " + type + "()");
};
{{format=xml}}
Factory.create_command_from_xml = function (payload)
{
};

Factory.serialize_command_to_xml = function (command)
{
};

Factory.clone_object = function (obj)
{
    let payload = Factory.serialize_command_to_xml(obj);
    return Factory.create_command_from_xml(payload);
};
{{end_format=xml}}
{{format=json}}
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
{{end_format=json}}
{{format=both}}
Factory.create_command_from_xml = function (payload)
{
};

Factory.serialize_command_to_xml = function (command)
{
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
{{end_format=both}}

'''
