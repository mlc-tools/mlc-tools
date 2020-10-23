import sys
import re


class RegexPatternPython(object):

    def __init__(self):
        pass

    regs_class_names = {}

    FACTORY = re.compile(r'\bFactory\b')

    FUNCTION = (
        (re.compile(r'DataStorage::shared\(\).get<(\w+)>'), r'DataStorage::shared().get\1', ['DataStorage::shared']),
        (re.compile(r'Factory::(.+)<\w+>'), r'Factory.\1', ['Factory::']),
        (re.compile(r'for\s*\(\s*\w+[\s&\*]*(\w+)\s*:\s*(.+)\s*\)'), r'for \1 in \2:', ['for']),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+<([\.\->\w]+?);\s*\+\+\w+\s*\)'),
         r'for \1 in range(int(\2), int(\3)):', ['for']),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+>([\.\->\w]+?);\s*--\w+\s*\)'),
         r'for \1 in range(int(\2), int(\3), -1):',
         ['for']),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+<([\.\->\w]+?);\s*\w+\+=(\w+)\s*\)'),
         r'for \1 in range(int(\2), int(\3), int(\4)):', ['for']),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+>([\.\->\w]+?);\s*\w+-=(\w+)\s*\)'),
         r'for \1 in range(int(\2), int(\3), -int(\4)):', ['for']),
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)'),
         r'for \1, \2 in \3.items():' if sys.version_info[0] == 3 else r'for \1, \2 in \3.iteritems():', ['for']),
        (re.compile(r'\bwhile\s*\((.+)\)'), r'while(\1):', ['while']),
        (re.compile(r'else\s+if\s*\(\s*(.+)\s*\)'), r'elif \1:', ['else']),
        (re.compile(r'if\s*\(\s*(.+)\s*\)'), r'if \1:', ['if']),
        (re.compile(r'if\s*!(.+):'), r'if not \1:', ['if']),
        (re.compile(r'else'), r'else:', ['else']),
        (re.compile(r'std::string (\w+);'), r'\1 = ""', ['std::string']),
        (re.compile(r'(\w+)\s+(\w+);'), r'\2 = \1()'),
        (re.compile(r'(\w+) = return\(\)'), r'return \1', ['return']),
        (re.compile(r'std::vector<.+>\s+(\w+)'), r'\1 = list()', ['std::vector']),
        (re.compile(r'std::string\s+(\w+)'), r'\1', ['std::string']),
        (re.compile(r'\blist<.+>\s+(\w+)'), r'\1 = list()', ['list<']),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'\3 = dict()', ['map<']),

        # nullish coalescing operator
        # auto c = test->a ?? test->b;
        # https://trello.com/c/WPR70BUY/37-add-operator
        (re.compile(r'[\w\*]+ ([\w\->\.]+)\s*=\s*([\w\->\.]+)\s*\?\?\s*([\w\->\.]+)'),
         r'\1 = (\2) if (\2 is not None) else (\3)', ['??']),

        (re.compile(r'\bauto\&* (\w+)'), r'\1', ['auto']),
        (re.compile(r'\bstring (\w+)'), r'\1', ['string']),
        (re.compile(r'\bint (\w+)'), r'\1', ['int']),
        (re.compile(r'\bfloat (\w+)'), r'\1', ['float']),
        (re.compile(r'\bbool (\w+)'), r'\1', ['bool']),
        (re.compile(r'std::min<int>'), r'std::min', ['std::min']),
        (re.compile(r'std::min<float>'), r'std::min', ['std::min']),
        (re.compile(r'std::max<int>'), r'std::max', ['std::max']),
        (re.compile(r'std::max<float>'), r'std::max', ['std::max']),
        (re.compile(r'\b\w+ (\w+)\s+=\s+(.+);'), r'\1 = \2', ['=']),
        (re.compile(r'(\w)->'), r'\1.'),
        (re.compile(r'\+\+(\w+)'), r'\1 += 1'),
        (re.compile(r'(\w+)\+\+'), r'\1 += 1'),
        (re.compile(r'delete (\w*);'), 'pass'),
        (re.compile(r'&(\w+)'), r'\1'),
        (re.compile(r'!(\w+)'), r'not \1'),
        (re.compile(r'!\('), r'not ('),
        (re.compile(r'make_intrusive<(\w+)>\(\)'), r'\1()', ['make_intrusive']),
        (re.compile(r'new\s*(\w+)\s*\((.*?)\)'), r'\1(\2)', ['new']),
        (re.compile(r'assert\(.+\);'), r'', ['assert ']),
        (re.compile(r'(\b[-0-9]+)\.f\b'), r'\1.0'),
        (re.compile(r'(\b[-0-9]+)\.([-0-9]*)f\b'), r'\1.\2'),
        (re.compile(r'([*+-/\s])log\((.+?)\)'), r'\1math.log(\2)', ['log']),
        (re.compile(r'random_float\(\)'), 'random.random()', ['random_float']),
        (re.compile(r'random_int\((.+)?,\s*(.+)?\)'), r'random.randint(\1, \2 - 1)', ['random_int']),
        (re.compile(r'\bthis\b'), r'self', ['this']),
        (re.compile(r', std::placeholders::_\d'), r'', ['std::placeholders']),
        (re.compile(r'dynamic_pointer_cast_intrusive<(\w+),\s*(\w+)>\((.+?)\)'),
         r'(\3 if isinstance(\3, \1) else None)', ['dynamic_pointer_cast_intrusive']),
        (re.compile(r'dynamic_pointer_cast_intrusive<(.+)>\((.+?)\)'), r'(\2 if isinstance(\2, \1) else None)',
         ['dynamic_pointer_cast_intrusive']),
        (re.compile(r'([\w\.]+?)\s*!=\s*False'), r'(\1)', ['False']),
        (re.compile(r'([\w\.]+?)\s*==\s*False'), r'not (\1)', ['False']),
        (re.compile(r'\bstrTo<(\w+)>\((.+?)\)'), r'strTo(\2, \1)', ['strTo']),
        (re.compile(r'\btoStr\((.+?)\)'), r'str(\1)', ['toStr']),
        (re.compile(r'(\w+)<(.+)>\((.+?)\)'), r'\1(\3, \2)', ['<']),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'((\1)+(\2))', ['std::strcat']),
        (re.compile(r'\.at\((.*?)\)'), r'[\1]', ['at']),

        # Exception with try/catch block (one catch)
        (re.compile(r'try\n\s*{([\s\S.]+?)}\n\s*catch\(((\w+)\s*(\w*))\)\n\s+{([\s\S.]+?)}'),
         r'try:\n{\n\1\n}\nexcept BaseException as \4:\n{\n\5\n}\n', ['try']),
        (re.compile(r'throw Exception\((.*?)\)'), r'raise BaseException()', ['throw']),
    )

    PEP8 = (
        (re.compile(r'([\w\.]+?)\s*!=\s*False'), r'(\1)'),
        (re.compile(r'([\w\.]+?)\s*==\s*False'), r'not (\1)'),
        (re.compile(r'([\w\.]+?)\s*!=\s*True'), r'not (\1)'),
        (re.compile(r'([\w\.]+?)\s*==\s*True'), r'(\1)'),
    )

    REPLACES = (
        ('this.', 'self.'),
        ('->', '.'),
        ('::', '.'),
        ('&&', ' and '),
        ('||', ' or '),
        ('  and  ', ' and '),
        ('  or  ', ' or '),
        ('true', 'True'),
        ('false', 'False'),
        ('nullptr', 'None'),
        ('std.round', 'int'),
        ('std.fabs', 'abs'),
        ('std.ceil', 'math.ceil'),
        ('std.floor', 'math.floor'),
        ('std.sqrt', 'math.sqrt'),
        ('std.min', 'min'),
        ('std.max', 'max'),
        ('!= None', 'is not None'),
        ('== None', 'is None'),
        (';', ''),
    )
