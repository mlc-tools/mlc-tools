FACTORY = '''
class Factory
{
}
Factory.build = function (type)
{
    return eval("new " + type + "()");
};

'''

COMMON = '''
create_command_from_json = function (payload)
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

serialize_command_to_json = function (command)
{
    let json = {};
    json[command.get_type()] = {};
    command.serialize_json(json[command.get_type()]);
    return JSON.stringify(json);
};

clone_object = function (obj)
{
    let payload = serialize_command_to_json(obj);
    return create_command_from_json(payload);
};
'''