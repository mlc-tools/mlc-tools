import re


class RegexPatternCpp(object):
    convert_c17_to_c14 = [
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)\s*{'),
         r'''for (auto&& pair : \3) \n{ \nauto& \1 = pair.first; \nauto& \2 = pair.second;
         (void)\1; //don't generate 'Unused variable' warning
         (void)\2; //don't generate 'Unused variable' warning''')
    ]

    FUNC_ARGS = (re.compile(r'\s*=\s*.+'), r'')

    FUNCTION = [
        (re.compile(r'new\s*(\w+)\s*\(\s*\)'), r'make_intrusive<\1>()'),
        (re.compile(r'\blist<([<:>\w\s\*&]+)>\s*(\w+)'), r'std::vector<\1> \2'),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'std::map<\1, \2> \3'),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'(std::string(\1) + std::string(\2))'),
        (re.compile(r'std::std::'), r'std::'),
    ]

    REPLACES = [
        ('std::round', 'round')
    ]