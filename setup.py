from setuptools import setup, find_packages
from os.path import join, dirname
import mlc_tools.version

setup(
    name='mlc-tools',
    version=mlc_tools.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    install_requires=[
    ]
    # entry_points={
    #     'console_scripts':
    #         ['mlc-tools = mlc_tools.main:console']
    # },
    # test_suite='tests'
)


# find_packages(package_dir)
