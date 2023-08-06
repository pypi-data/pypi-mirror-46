import os
import re

from setuptools import setup, find_packages


def readme():
    path = os.path.abspath(os.path.dirname(__file__))
    try:
        with open(os.path.join(path, 'README.md'), encoding='utf-8') as fp:
            long_description = '\n' + fp.read()
    except FileNotFoundError:
        long_description = 'Python CLI for previewing and running Pipfile scripts'
    return long_description


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'pps', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in pps/__init__.py')


setup(
    name='preview-pipfile-scripts',
    author='Seunguk Lee',
    author_email='lsy931106@gmail.com',
    description='Python CLI for previewing and running Pipfile scripts',
    long_description=readme(),
    long_description_content_type='text/markdown',
    license='MIT',
    version=read_version(),
    url='https://github.com/SeungUkLee/pps',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
    ],
    entry_points={
        'console_scripts': [
            'pps = pps.cli:main',
        ],
    },
    install_requires=[
        'inquirer==2.5.1',
        'toml==0.10.0',
    ]
)
