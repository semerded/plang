from setuptools import find_packages, setup

setup(
    name='plang',
    packages=find_packages(exclude=""),
    version='0.1.0',
    description='plang (Python Library for Apps N Games) is build on top of Pygame 2 (using SDL 2) with highly optimized and user friendly codebase.',
    author='Sem Van Broekhoven',
    install_requires=['colorama', 'typing_extensions', 'cffi'],
)