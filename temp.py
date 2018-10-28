from mlc_tools import Mlc
import os


def python():
    root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
    mlc = Mlc()
    
    mlc.additional_config_directories.append(root + 'tests/simple_test/config_additional')
    mlc.generate(language='py',
                 configs_directory=root + 'tests/simple_test/config',
                 out_directory=root + 'tests/simple_test/generated_py',
                 side='client'
                 )
    
    mlc.additional_data_directories.append(root + 'tests/simple_test/data_additional')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_xml/',
                      out_data_directory='tests/simple_test/assets')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_json/',
                      out_data_directory='tests/simple_test/assets')
    python_test()
    

def python_test():
    root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
    mlc = Mlc()
    mlc.run_test(test_script=root + 'tests/simple_test/test_py.py', test_script_args='json')
    mlc.run_test(test_script=root + 'tests/simple_test/test_py.py', test_script_args='xml')


def php():
    root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
    mlc = Mlc()
    
    mlc.additional_config_directories.append(root + 'tests/simple_test/config_additional')
    mlc.generate(language='php',
                 configs_directory=root + 'tests/simple_test/config',
                 out_directory=root + 'tests/simple_test/generated_php',
                 side='server'
                 )
    
    mlc.additional_data_directories.append(root + 'tests/simple_test/data_additional')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_xml/',
                      out_data_directory='tests/simple_test/assets')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_json/',
                      out_data_directory='tests/simple_test/assets')
    mlc.run_test(test_script=root + 'tests/simple_test/test_php.py', test_script_args='json')
    # mlc.run_test(test_script=root + 'tests/simple_test/test_php.py', test_script_args='xml')

    
def cpp():
    root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
    mlc = Mlc()
    
    mlc.additional_config_directories.append(root + 'tests/simple_test/config_additional')
    mlc.generate(language='cpp',
                 configs_directory=root + 'tests/simple_test/config',
                 out_directory=root + 'tests/simple_test/generated_cpp/xml',
                 side='client'
                 )
    
    mlc.additional_data_directories.append(root + 'tests/simple_test/data_additional')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_xml/',
                      out_data_directory='tests/simple_test/assets')
    mlc.generate_data(data_directory=root + 'tests/simple_test/data_json/',
                      out_data_directory='tests/simple_test/assets')
    
    # mlc.run_test(test_script=root + 'tests/simple_test/test_cpp.py', test_script_args='json')
    mlc.run_test(test_script=root + 'tests/simple_test/test_cpp.py', test_script_args='xml')


def profile(func_to_profile):
    def get_profile_(func):
        """ Returns performance statistics (as a string) for the given function.
        """
        def _run():
            func()
        import cProfile as profile
        import pstats
        import os
        import sys
        sys.modules['__main__'].__profile_run__ = _run
        id = func.__name__ + '()'
        profile.run('__profile_run__()', id)
        p = pstats.Stats(id)
        p.stream = open(id, 'w')
        p.sort_stats('time').print_stats(20)
        p.stream.close()
        s = open(id).read()
        os.remove(id)
        return s
    print(get_profile_(func_to_profile))


# profile(cpp)
# profile(python)
# profile(python_test)
python()
cpp()