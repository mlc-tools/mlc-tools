from mlc_tools import Mlc
import os

root = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + '/'
mlc = Mlc()
mlc.additional_config_directories.append(root + 'tests/simple_test/config_additional')
mlc.generate(language='py',
             format='xml',
             configs_directory=root + 'tests/simple_test/config',
             out_directory=root + 'temp/generated_py')
