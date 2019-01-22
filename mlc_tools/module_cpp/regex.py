import re


class RegexPatternCpp(object):
    regs_class_names = {}

    convert_c17_to_c14 = [
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)\s*{'),
         r'''for (auto&& pair : \3) \n{ \nauto& \1 = pair.first; \nauto& \2 = pair.second;
         (void)\1; //don't generate 'Unused variable' warning
         (void)\2; //don't generate 'Unused variable' warning''', ['for'])
    ]

    FUNC_ARGS = (re.compile(r'\s*=\s*.+'), r'')

    FUNCTION = [
        (re.compile(r'throw new Exception\((.*?)\)'), r'throw std::exception(\1)', ['throw ']),
        (re.compile(r'(\w+)\*\s+(\w+) = new\s*(\w+)\s*\(\s*\)'), r'auto \2 = make_intrusive<\3>()', ['new']),
        (re.compile(r'new\s*(\w+)\s*\(\s*\)'), r'make_intrusive<\1>()', ['new']),
        (re.compile(r'\blist<([<:>\w\s\*&]+)>\s*(\w+)'), r'std::vector<\1> \2', ['list<']),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'std::map<\1, \2> \3', ['map<']),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'(std::string(\1) + std::string(\2))', ['std::strcat']),
        (re.compile(r'std::std::'), r'std::', ['std::std']),

        # Exception with try/catch block (one catch)
        (re.compile(r'try\n\s*{([\s\S.]+?)}\n\s*catch\(((\w+)\s*(\w*))\)\n\s+{([\s\S.]+?)}'),
         r'try\n{\1}\ncatch(const std::exception& \4)\n{\5}', ['try', 'catch']),
    ]

    REPLACES = [
        ('std::round', 'round')
    ]
