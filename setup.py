from importlib.machinery import SourceFileLoader
from pathlib import Path
from setuptools import setup

description = 'Numerous useful plugins for pytest.'
long_description = Path(__file__).resolve().parent.joinpath('README.rst').read_text()

# importing just this file avoids importing the full package with external dependencies which might not be installed
version = SourceFileLoader('version', 'pytest_toolbox/version.py').load_module()

setup(
    name='pytest-toolbox',
    version=str(version.VERSION),
    description=description,
    long_description=long_description,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Testing',
        'Framework :: Pytest',
    ],
    keywords='pytest,plugin,toolbox',
    author='Samuel Colvin',
    license='MIT',
    author_email='S@muelColvin.com',
    url='https://github.com/samuelcolvin/pytest-toolbox',
    packages=['pytest_toolbox'],
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'pytest>=3.0.5',
    ],
    entry_points={
        'pytest11': ['toolbox = pytest_toolbox'],
    },
)
