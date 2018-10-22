import re


def smart_split(string, divider):
    assert(len(divider) == 1)
    if not string:
        return []

    parts = []
    depth = 0
    start = 0
    for curr, s in enumerate(string):
        if start >= curr:
            continue

        if s == divider and depth == 0:
            parts.append(string[start:curr - start])
            start = curr + 1
        elif s == '<':
            depth += 1
        elif s == '>':
            depth -= 1
    parts.append(string[start:])
    return parts


def parse_object_with_name(obj, string):
    if not string:
        return obj

    pattern_without_name = re.compile(r'([\w:*]+)([<\.:*&\w ,>]*)')
    pattern_with_name = re.compile(r'([\w:*]+)([<\.:*&\w ,>]*) +(\w+)')
    with_name = True
    try:
        parts = pattern_with_name.findall(string)
        if len(parts) == 0:
            with_name = False
            parts = pattern_without_name.findall(string)
        parts = parts[0]
    except IndexError as e:
        print(e)
        print(string)
        exit(1)
    obj.type = parts[0]
    if with_name:
        obj.name = parts[2]

    args = parts[1].strip()
    if args.startswith('<') and args.endswith('>'):
        args = args[1:-1]
    obj.template_args = smart_split(args, ',')
    obj.template_args = [x.strip() for x in obj.template_args]

    return obj


def tests():
    from .Object import Object

    def test_0():
        string = 'int a'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'a' and obj.type == 'int' and obj.template_args == []

    def test_1():
        string = 'list<list<int>> a'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'a' and obj.type == 'list' and obj.template_args == ['list<int>']

    def test_2():
        string = 'map<int, list<int>> foo'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'foo' and obj.type == 'map' and obj.template_args == ['int', 'list<int>']

    def test_3():
        string = 'map<int, DataReward*:link> foo'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'foo' and obj.type == 'map' and obj.template_args == ['int', 'DataReward*:link']

    def test_4():
        string = 'list<int>'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.type == 'list' and obj.template_args == ['int']

    def test_5():
        string = 'int'
        obj = parse_object_with_name(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == '' and obj.type == 'int' and obj.template_args == []

    print(test_0())
    print(test_1())
    print(test_2())
    print(test_3())
    print(test_4())
    print(test_5())


if __name__ == '__main__':
    tests()
