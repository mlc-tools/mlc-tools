import re


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

