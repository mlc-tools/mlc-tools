import re


def smart_split(string, divider):
    assert len(divider) == 1
    if not string:
        return []

    parts = []
    depth = 0
    start = 0
    for curr, char in enumerate(string):
        if start >= curr:
            continue

        if char == divider and depth == 0:
            parts.append(string[start:curr])
            start = curr + 1
        elif char in '<(':
            depth += 1
        elif char in '>)':
            depth -= 1
    parts.append(string[start:])
    return parts


def parse_object(obj, string):
    if not string:
        return obj

    # remove template
    templates = ''
    left = string.find('<')
    if left != -1:
        right = left
        size = len(string)
        i = left + 1
        counter = 1
        while i < size:
            if string[i] == '<':
                counter += 1
            if string[i] == '>':
                counter -= 1
            if counter == 0:
                right = i
                break
            i += 1
        if counter == 0 and right != left:
            templates = string[left+1:right]
            string = string[:left] + string[right+1:]

    args = re.search(r'\(.*\)', string)
    args = args.group(0) if args else None
    if args:
        string = string.replace(args, '')
    type_s = re.search(r'\w+[&\*]*', string).group(0)
    string = string[len(type_s):]
    while True:
        match = re.search(r':\w+', string)
        if not match:
            break
        modifier = match.group(0)
        string = string[len(modifier):]
        type_s += modifier

    name_s = string.strip()

    obj.type = type_s + (args if args else '')
    obj.name = name_s

    obj.template_args = smart_split(templates, ',')
    obj.template_args = [x.strip() for x in obj.template_args]

    return obj


def tests():
    from ..core.object import Object

    def test_0():
        string = 'int a'
        obj = parse_object(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'a' and obj.type == 'int' and obj.template_args == []

    def test_1():
        string = 'list<list<int>> a'
        obj = parse_object(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'a' and obj.type == 'list' and obj.template_args == ['list<int>']

    def test_2():
        string = 'map<int, list<int>> foo'
        obj = parse_object(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'foo' and obj.type == 'map' and obj.template_args == ['int', 'list<int>']

    def test_3():
        string = 'map<int, DataReward*:link> foo'
        obj = parse_object(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.name == 'foo' and obj.type == 'map' and obj.template_args == ['int', 'DataReward*:link']

    def test_4():
        string = 'list<int>'
        obj = parse_object(Object(), string)
        # print(obj.name)
        # print(obj.type)
        # print(obj.template_args)
        return obj.type == 'list' and obj.template_args == ['int']

    def test_5():
        string = 'int'
        obj = parse_object(Object(), string)
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
