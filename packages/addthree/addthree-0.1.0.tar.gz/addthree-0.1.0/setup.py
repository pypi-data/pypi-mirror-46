import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
DESCRIPTION = 'Practice deploying to PyPI'
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as fp:
        long_description = '\n' + fp.read()
except FileNotFoundError:
    long_description = DESCRIPTION


# def read(f):
#     return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'addthree', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in addthree/__init__.py')


setup(
    name='addthree',
    author='test',
    author_email='dltmddnr5' '@' 'naver.com',
    description='Practice deploying to PyPI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    version=read_version(),
    url='https://github.com/SeungUkLee/travis-practice',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
    ],
)
