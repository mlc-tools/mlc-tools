

class GeneratorFunctions(object):
    def __init__(self):
        pass

    @staticmethod
    def generate(model):
        model.add_file(None, 'functions.js', FUNCTIONS)


FUNCTIONS = '''
length_of = function (obj)
{
    return obj.length;
};

compare = function (lhs, rhs)
{
    if(!lhs || !rhs)
    {
        return lhs === rhs;
    }
    return lhs.valueOf() === rhs.valueOf();
};
'''