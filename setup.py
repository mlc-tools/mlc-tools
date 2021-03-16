import setuptools
import mlc_tools.version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlc-tools",
    version=mlc_tools.version,
    author="Vladimir Tolmachev",
    author_email="tolm_vl@hotmail.com",
    description="A tool to generate and translate C++ code to other languages from one code-base.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mlc-tools/mlc-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'mlc = mlc_tools.console.console:main'
        ]
    },
    python_requires='>=3.6',
)