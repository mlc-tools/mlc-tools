import inspect


class Color:

    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    light_grey = '\033[37m'
    endc = '\033[0m'


class Log:

    use_colors = True
    disable_logs = False

    @staticmethod
    def debug(msg):
        if not Log.disable_logs:
            print(Color.light_grey + msg + Color.endc) if Log.use_colors else msg

    @staticmethod
    def error(msg):
        if not Log.disable_logs:
            print(Color.red + msg + Color.endc) if Log.use_colors else msg

    @staticmethod
    def warning(msg):
        if not Log.disable_logs:
            print(Color.orange + msg + Color.endc) if Log.use_colors else msg

    @staticmethod
    def message(msg):
        if not Log.disable_logs:
            print(Color.green + msg + Color.endc) if Log.use_colors else msg


class Error:
    UNKNOWN_SERIALISED_TYPE = inspect.currentframe().f_lineno
    STATIS_MEMBER_SHOULD_HAVE_INITIALISATION = inspect.currentframe().f_lineno
    MAP_TWO_ARGS = inspect.currentframe().f_lineno
    DUBLICATE_METHODS = inspect.currentframe().f_lineno
    DUBLICATE_CLASS = inspect.currentframe().f_lineno
    UNKNOWN_BEHAVIOR = inspect.currentframe().f_lineno
    UNKNOWN_CLASS = inspect.currentframe().f_lineno
    CANNOT_FIND_CLASS_FOR_METHOD = inspect.currentframe().f_lineno
    CANNOT_FIND_CLASS_FOR_OBJECT = inspect.currentframe().f_lineno
    OBJECT_IS_KEY_OF_MAP = inspect.currentframe().f_lineno
    CANNOT_PARSE_XML = inspect.currentframe().f_lineno
    ENUM_CANNOT_BE_COMBINATED = inspect.currentframe().f_lineno

    texts = {
        UNKNOWN_SERIALISED_TYPE: '[{}] unknown serialized serialized format. Base type - [{}]',
        STATIS_MEMBER_SHOULD_HAVE_INITIALISATION: 'Static method have to have a initial value. [{}::{}]',
        MAP_TWO_ARGS: 'Map have to have 2 arguments. [{}::{}]',
        DUBLICATE_METHODS: 'duplication function in one class [{}::{}]',
        DUBLICATE_CLASS: 'Duplication classes [{}]',
        UNKNOWN_BEHAVIOR: 'Cannot find behavior class: {}<{}>',
        UNKNOWN_CLASS: 'Unknown class: {}',
        CANNOT_FIND_CLASS_FOR_METHOD: 'Cannot find class [{}] for method [{}]',
        CANNOT_FIND_CLASS_FOR_OBJECT: 'Cannot find class [{}] for object [{}]',
        OBJECT_IS_KEY_OF_MAP: 'Validate php feature: key of array cannot be object [{}::map<{}, {}> {}]',
        CANNOT_PARSE_XML: 'Error on parsing xml [{}]',
        ENUM_CANNOT_BE_COMBINATED: 'Enum member [{}::{}] cannot be initialed by [{}] value',
    }

    @staticmethod
    def exit(*args):
        Log.error((' Error {}: ' + Error.texts[args[0]]).format(args[0], *args[1:]))
        exit(args[0])

    @staticmethod
    def warning(*args):
        Log.warning((' Warning {}: ' + Error.texts[args[0]]).format(args[0], *args[1:]))
