
CLASS_FUNCTION_GET_TYPE = 'get_type'
CLASS_FUNCTION_GET_PROPERTY = 'get_property'
CLASS_FUNCTION_SET_PROPERTY = 'set_property'


class Modifier:

    def __init__(self):
        pass

    abstract = ':abstract'
    serialized = ':serialized'
    static = ':static'
    const = ':const'
    external = ':external'
    visitor = ':visitor'
    set_function = ':set_function'
    runtime = ':runtime'
    key = ':key'
    link = ':link'
    storage = ":storage"
    private = ":private"

    client = ':client'
    server = ':server'
    side_client = 'client'
    side_server = 'server'
