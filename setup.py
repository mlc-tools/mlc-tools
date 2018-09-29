from setuptools import setup, find_packages
import mlc_tools.version

setup(
    name='mlc-tools',
    version=mlc_tools.__version__,
    packages=find_packages(),
    long_description="mlc-tools",
    install_requires=[
    ]
    # entry_points={
    #     'console_scripts':
    #         ['mlc-tools = mlc_tools.main:console']
    # },
    # test_suite='tests'
)
