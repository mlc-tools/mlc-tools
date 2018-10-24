from mlc_tools import Mlc
import os

root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
mlc = Mlc()

mlc.additional_config_directories.append(root + 'tests/simple_test/config_additional')
mlc.generate(language='py',
             configs_directory=root + 'tests/simple_test/config',
             out_directory=root + 'tests/simple_test/generated_py')

mlc.additional_data_directories.append(root + 'tests/simple_test/data_additional')
mlc.generate_data(data_directory=root + 'tests/simple_test/data_xml/',
                  out_data_directory='tests/simple_test/assets')
mlc.generate_data(data_directory=root + 'tests/simple_test/data_json/',
                  out_data_directory='tests/simple_test/assets')

mlc.run_test(test_script=root + 'tests/simple_test/test_py.py', test_script_args='json')
mlc.run_test(test_script=root + 'tests/simple_test/test_py.py', test_script_args='xml')
