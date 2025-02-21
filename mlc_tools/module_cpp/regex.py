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

        # lambdas
        # FROM:
        #   map_remove_if(this->test_models, (key, value :> value->data == nullptr));
        (re.compile(r'map_remove_if\(([\w\d\-\>\.\[\]]+),\s*\((\w+),\s*(\w+)\s*:>\s*(.+)\)\)'),
         r'''for(auto __iter__ = \1.begin(); __iter__ != \1.end();)
{
    auto& \2 = __iter__->first; auto& \3 = __iter__->second; (void)\2;(void)\3;
    if(\4) __iter__ = \1.erase(__iter__);
    else ++__iter__;
}''', ['map_remove_if']),

        # FROM:
        #   list_remove_if(this->test_list_lambda, (value :> value == 3));
        (re.compile(r'list_remove_if\(([\w\d\-\>\[\]]+),\s*\((\w+)\s*:>\s*(.+)\)\)'), r'''
auto iter = std::remove_if(\1.begin(), \1.end(), [&](const auto& \2)
{
    return \3;
});
\1.erase(iter, \1.end())
''', ['list_remove_if']),

        # lambdas
        # FROM:
        #   map_do_if(this->test_models, (key, value :> value->data == nullptr :> some_action));
        (re.compile(r'map_do_if\(([\w\d\-\>\.\[\]]+),\s*\((\w+),\s*(\w+?)\s*:>\s*(.+?):>\s*(.+)\)\);'),
         r'''for(auto __iter__ = \1.begin(); __iter__ != \1.end();)
{
    auto& \2 = __iter__->first; auto& \3 = __iter__->second; (void)\2;(void)\3;
    if(\4) {++__iter__; \5;}
    else ++__iter__;
}''', ['map_do_if']),

        # FROM:
        #   list_do_if(this->test_list_lambda, (value :> value == 3 :> some_action);
        (re.compile(r'list_do_if\(([\w\d\-\>\.\[\]]+),\s*\((\w+)\s*:>\s*(.+?):>\s*(.+)\)\);'), r'''
        for(int __index__ = 0; __index__ < \1.size(); ++__index__)
        {
            auto& \2 = \1.at(__index__);
            if(\3)
            {
                auto __size__ = \1.size();
                \4;
                if(__size__ != \1.size())
                {
                    __index__ -= 1;
                }
            }
        }''', ['list_do_if']),

        # FROM:
        #   list_do(this->test_list_lambda, (value :> some_action);
        (re.compile(r'list_do\(([\w\d\-\>\.\[\]]+),\s*\((\w+)\s*:>\s*(.+)\)\)'), r'''
        for(int __index__ = 0; __index__ < \1.size(); ++__index__)
        {
            auto& \2 = \1.at(__index__);
            \3;
        }''', ['list_do']),

        (re.compile(r'throw new Exception\((.*?)\)'), r'throw std::exception(\1)', ['throw ']),
        (re.compile(r'(\w+)\*\s+(\w+) = new\s*(\w+)\s*\(\s*\)'), r'auto \2 = make_intrusive<\3>()', ['new']),
        (re.compile(r'\bnew\s*(\w+)\s*\((.*)\)'), r'make_intrusive<\1>(\2)', ['new']),
        (re.compile(r'\blist<([<:>\w\s\*&]+)>\s*(\w+)'), r'std::vector<\1> \2', ['list<']),
        (re.compile(r'\bmap<([<:>\w\s\*&]+),\s*([<:>\w\s\*&]+)>\s*(\w+)'), r'std::map<\1, \2> \3', ['map<']),
        (re.compile(r'std::strcat\((.+?),\s*(.+?)\)'), r'(std::string(\1) + std::string(\2))', ['std::strcat']),
        (re.compile(r'std::std::'), r'std::', ['std::std']),
        (re.compile(r'([\w\->\.]+)\s*=\s*([\w\->\.]+)\s*\?\?\s*([\w\->\.]+)'), r'\1 = (\2 != nullptr) ? \2 : (\3)', ['??']),
        (re.compile(r'\bprint\s*\(\s*(.+)\);'), r'std::cout << format(\1) << std::endl;', ['print']),

        # Exception with try/catch block (one catch)
        (re.compile(r'try\n\s*{([\s\S.]+?)}\n\s*catch\(((\w+)\s*(\w*))\)\n\s+{([\s\S.]+?)}'),
         r'try\n{\1}\ncatch(const std::exception& \4)\n{\5}', ['try', 'catch']),
    ]

    REPLACES = [
        ('std::round', 'round')
    ]
