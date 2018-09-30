import sys
import re


class RegexPatternPython:
    FACTORY = re.compile(r'\bFactory\b')
    ET = re.compile(r'\bET\.')
    FUNCTION = (
        (re.compile(r'DataStorage::shared\(\).get<(\w+)>'), r'DataStorage::shared().get\1'),
        (re.compile(r'Factory::(.+)<\w+>'), r'Factory.\1'),
        (re.compile(r'for\s*\(\s*\w+[\s&\*]*(\w+)\s*:\s*(.+)\s*\)'), r'for \1 in \2:'),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+<(\w+);\s*\+\+\w+\s*\)'), r'for \1 in range(\2, int(\3)):'),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+>(\w+);\s*--\w+\s*\)'), r'for \1 in range(\2, int(\3), -1):'),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+<(\w+);\s*\w+\+=(\w)\s*\)'), r'for \1 in range(\2, int(\3), \4):'),
        (re.compile(r'for\s*\(\s*\w+\s*(\w+)=(\w+);\s*\w+>(\w+);\s*\w+-=(\w)\s*\)'), r'for \1 in range(\2, int(\3), -\4):'),
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)'),
         r'for \1, \2 in \3.items():' if sys.version_info[0] == 3 else r'for \1, \2 in \3.iteritems():'),
        (re.compile(r'\bwhile\s*\((.+)\)'), r'while(\1):'),
        (re.compile(r'else\s+if\s*\(\s*(.+)\s*\)'), r'elif \1:'),
        (re.compile(r'if\s*\(\s*(.+)\s*\)'), r'if \1:'),
        (re.compile(r'if\s*!(.+):'), r'if not \1:'),
        (re.compile(r'else'), r'else:'),
        (re.compile(r'in_map\s*\(\s*(.+),\s*(.+)\s*\)'), r'(\1 in \2)'),
        (re.compile(r'in_list\s*\(\s*(.+),\s*(.+)\s*\)'), r'(\1 in \2)'),
        (re.compile(r'list_push\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1.append(\2)'),
        (re.compile(r'list_remove\s*\(\s*(.+),\s*(.+)\s*\)'), r'\1.remove(\2)'),
        (re.compile(r'list_clear\s*\(\s*(.+)\s*\)'), r'\1 = list()'),
        (re.compile(r'list_size\s*\('), r'len('),
        (re.compile(r'map_size\s*\('), r'len('),
        (re.compile(r'string_empty\((.+?)\)'), r'(not (\1))'),
        (re.compile(r'string_size\((.+?)\)'), r'len(\1)'),
        (re.compile(r'(\w+)\s+(\w+);'), r'\2 = \1()'),
        (re.compile(r'(\w+) = return\(\)'), r'return \1'),
        (re.compile(r'std::vector<.+>\s+(\w+)'), r'\1 = list()'),
        (re.compile(r'std::string\s+(\w+)'), r'\1'),
        (re.compile(r'\blist<.+>\s+(\w+)'), r'\1 = list()'),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'\3 = dict()'),
        (re.compile(r'auto\&* (\w+)'), r'\1'),
        (re.compile(r'string (\w+)'), r'\1'),
        (re.compile(r'int (\w+)'), r'\1'),
        (re.compile(r'float (\w+)'), r'\1'),
        (re.compile(r'bool (\w+)'), r'\1'),
        (re.compile(r'(\w)->'), r'\1.'),
        (re.compile(r'\+\+(\w+)'), r'\1 += 1'),
        (re.compile(r'(\w+)\+\+'), r'\1 += 1'),
        (re.compile(r'delete (\w*);'), 'pass'),
        (re.compile(r'&(\w+)'), r'\1'),
        (re.compile(r'!(\w+)'), r'not \1'),
        (re.compile(r'!\('), r'not ('),
        (re.compile(r'make_intrusive<(\w+)>\(\)'), r'\1()'),
        (re.compile(r'new\s*(\w+)\s*\(\s*\)'), r'\1()'),
        (re.compile(r'assert\(.+\);'), r''),
        (re.compile(r'(\b[-0-9]+)\.f\b'), r'\1.0'),
        (re.compile(r'(\b[-0-9]+)\.([-0-9]*)f\b'), r'\1.\2'),
        (re.compile(r';'), r''),
        (re.compile(r'([*+-/\s])log\((.+?)\)'), r'\1math.log(\2)'),
        (re.compile(r'random_float\(\)'), 'random.random()'),
        (re.compile(r'random_int\((.+)?,\s*(.+)?\)'), r'random.randint(\1, \2 - 1)'),
        (re.compile(r'\bthis\b'), r'self'),
        (re.compile(r', std::placeholders::_\d'), r''),
        (re.compile(r'dynamic_pointer_cast_intrusive<\w+>\((.+?)\)'), r'\1'),
        (re.compile(r'([\w\.]+?)\s*!=\s*False'), r'(\1)'),
        (re.compile(r'([\w\.]+?)\s*==\s*False'), r'not (\1)'),
        (re.compile(r'\bstrTo<(\w+)>\((.+?)\)'), r'\1(\2)'),
        (re.compile(r'\btoStr\((.+?)\)'), r'str(\1)'),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'((\1)+(\2))'),
        (re.compile(r'\.at\((.*?)\)'), r'[\1]'),
    )
    regs_class_names = {}

    PEP8 = (
        (re.compile(r'([\w\.]+?)\s*!=\s*False'), r'(\1)'),
        (re.compile(r'([\w\.]+?)\s*==\s*False'), r'not (\1)'),
    )
    REPLASES = (
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
        ('std.round', 'round'),
        ('std.fabs', 'abs'),
        ('std.ceil', 'math.ceil'),
        ('std.floor', 'math.floor'),
        ('std.sqrt', 'math.sqrt'),
        ('std.min<int>', 'min'),
        ('std.min<float>', 'min'),
        ('std.min', 'min'),
        ('std.max<int>', 'max'),
        ('std.max<float>', 'max'),
        ('std.max', 'max'),
        ('!= None', 'is not None'),
        ('== None', 'is None'),
    )


class RegexPatternPhp:

    FUNCTION = (
        (re.compile(r'DataStorage::shared\(\).get<(\w+)>'), r'DataStorage::shared()->get\1'),
        (re.compile(r'Factory::(.+)<\w+>'), r'Factory::\1'),
        (re.compile(r'\.str\(\)'), r''),
        (re.compile(r'for\s*\(auto (.+?)\s*:\s*(.+)\s*\)'), r'foreach($\2 as $\1)'),
        (re.compile(r'for\s*\(auto& (.+?)\s*:\s*(.+)\s*\)'), r'foreach($\2 as $\1)'),
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)'), r'foreach ($\3 as $\1 => $\2)'),
        (re.compile(r'auto (\w+)'), r'$\1'),
        (re.compile(r'auto& (\w+)'), r'$\1'),
        (re.compile(r'void (\w+)'), r'$\1'),
        (re.compile(r'int (\w+)'), r'$\1'),
        (re.compile(r'bool (\w+)'), r'$\1'),
        (re.compile(r'\((\w+) (\w+)\)'), r'($\2)'),
        (re.compile(r'\(const (\w+)\& (\w+)\)'), r'($\2)'),
        (re.compile(r'\(const (\w+)\* (\w+)\)'), r'($\2)'),
        (re.compile(r'\((\w+)\* (\w+)\)'), r'($\2)'),
        (re.compile(r'(\w+)\ (\w+),'), r'$\2,'),
        (re.compile(r'(\w+)\& (\w+),'), r'$\2,'),
        (re.compile(r'(\w+)\* (\w+),'), r'$\2,'),
        (re.compile(r'const (\w+)\* (\w+)'), r'$\2'),
        (re.compile(r'const (\w+)\& (\w+)'), r'$\2'),
        (re.compile(r'float (\w+)'), r'$\1'),
        (re.compile(r'std::string (\w+)'), r'$\1'),
        (re.compile(r'\bthis\b'), r'$this'),
        (re.compile(r':const'), r''),
        (re.compile(r'(\w+)::(\w+)'), r'\1::$\2'),
        (re.compile(r'(\w+)::(\w+)\)'), r'\1::$\2)'),
        (re.compile(r'(\w+)::(\w+)\.'), r'\1::$\2.'),
        (re.compile(r'(\w+)::(\w+)->'), r'\1::$\2->'),
        (re.compile(r'(\w+)::(\w+)\]'), r'\1::$\2]'),
        (re.compile(r'(\w+)::\$(\w+)\('), r'\1::\2('),
        (re.compile(r'(\w+)::\$(\w+)\((\w*)\)'), r'\1::\2(\3)'),
        (re.compile(r'function \$(\w+)'), r'function \1'),
        (re.compile(r'\.at\((.*?)\)'), r'[\1]'),
        (re.compile(r'(\w+)\.'), r'\1->'),
        (re.compile(r'(\w+)\(\)\.'), r'\1()->'),
        (re.compile(r'(\w+)\]\.'), r'\1]->'),
        (re.compile(r'&(\w+)'), r'\1'),
        (re.compile(r'\$if\('), r'if('),
        (re.compile(r'delete \$(\w+);'), r''),
        (re.compile(r'([-0-9])->([-0-9])f\b'), r'\1.\2'),
        (re.compile(r'assert\(.+\);'), r''),
        (re.compile(r'make_intrusive<(\w+)>\(\s*\)'), r'new \1()'),
        (re.compile(r'dynamic_pointer_cast_intrusive<\w+>\((.+?)\)'), r'\1'),
        (re.compile(r'new\s*(\w+)\s*\(\s*\)'), r'new \1()'),
        (re.compile(r'(.+?)\->push_back\((.+)\);'), r'array_push(\1, \2);'),
        (re.compile(r'(\w+)\s+(\w+);'), r'$\2 = new \1();'),
        (re.compile(r'\$(\w+) = new return\(\);'), r'return \1;'),
        (re.compile(r'std::\$vector<.+?>\s+(\w+)'), r'$\1 = array()'),
        (re.compile(r'\blist<.+>\s+(\w+)'), r'$\1 = array()'),
        (re.compile(r'\bmap<([<:>\w\s\*&\$]+),\s*([<:>\w\s\*&\$]+)>\s*(\w+)'), r'$\3 = array()'),
        (re.compile(r'\bstrTo<(\w+)>'), r'(\1)'),
        (re.compile(r'\btoStr\b'), r'(string)'),
        (re.compile(r'(@{__string_\d+__})\s*\+'), r'\1.'),
        (re.compile(r'\+\s*(@{__string_\d+__})'), r'.\1'),
    )

    FUNCTION_2 = (
        (re.compile(r'->\$(\w+)\('), r'->\1('),
        (re.compile(r'([-0-9]*)->([-0-9]*)f\b'), r'\1.\2'),
        (re.compile(r'([-0-9]*)->f\\b'), r'\1.0'),
        (re.compile(r'\$return\s'), r'return'),
        (re.compile(r'(\$.+)->add\((\$.+),\s*(\w+)::\$(\w+),\s*std::\$placeholders::\$_\d\);'), r'\1->add(\2, array(\2, "\4"));'),
        (re.compile(r'list_remove\((\$.+?),\s*(\$.+?)\);'), r'unset(\1[array_search(\2, \1)]);'),
        (re.compile(r'list_clear\((.+?)\);'), r'\1 = array();'),
        (re.compile(r'string_empty\((.+?)\)'), r'(count(\1) == 0)'),
        (re.compile(r'random_float\(\)'), r'(mt_rand() * 1.0 / mt_getrandmax())'),
        (re.compile(r'random_int\((.+?),\s*(.+)\)'), r'mt_rand(\1, \2-1)'),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'((\1).(\2))'),
    )

    VARIABLES = {
        re.compile(r'\$(\w+)'): {}
    }

    INITIALIZE = (re.compile(r'(\w+)::(\w+)'), r'\1::$\2')


class RegexPatternCpp:
    convert_c17_to_c14 = (
        (re.compile(r'for\s*\(auto&&\s*\[(\w+),\s*(\w+)\]\s*:\s*(.+)\)\s*{'), r'''for (auto&& pair : \3) \n{ \nauto& \1 = pair.first; \nauto& \2 = pair.second;
                           (void)\1; //don't generate 'Unused variable' warning
                           (void)\2; //don't generate 'Unused variable' warning''')
    )

    FUNC_ARGS = (re.compile(r'\s*=\s*.+'), r'')

    FUNCTION = [
        (re.compile(r'new\s*(\w+)\s*\(\s*\)'), r'make_intrusive<\1>()'),
        (re.compile(r'\blist<([<:>\w\s\*&]+)>\s*(\w+)'), r'std::vector<\1> \2'),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'std::map<\1, \2> \3'),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'(std::string(\1) + std::string(\2))'),
        (re.compile(r'std::std::'), r'std::'),
    ]
