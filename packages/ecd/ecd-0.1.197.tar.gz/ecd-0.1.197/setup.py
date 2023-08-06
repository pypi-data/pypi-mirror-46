# coding:utf-8
"""
author: sixi
datetime: 2019/03/11
python version: 3.x
summary: 
install package:
"""
import codecs
import os

from setuptools import find_packages, setup

from ecd import __version__

here = os.path.abspath(os.path.dirname(__file__))

def get_install_requires():
    with open(os.path.join(here, "requirements.txt"), 'r', encoding='utf-8') as fp:
        rows = fp.read()
    return list(filter(None, rows.split("\n")))

def read(*parts):
    try:
        with codecs.open(os.path.join(here, *parts), 'r', encoding="gbk") as fp:
            return fp.read()
    except UnicodeDecodeError:
        with codecs.open(os.path.join(here, *parts), 'r', encoding="utf-8") as fp:
            return fp.read()


long_description = read('README.md')

setup(
    name="ecd",
    version=__version__,
    description="the english translate tool",
    long_description=long_description,

    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    url='https://github.com/sixiyizai/ecd',
    keywords='english to chinese dictionary',

    author='sixiyizai',
    author_email='lingyunzou@aliyun.com',

    package_dir={"ecd": "ecd"},
    packages=find_packages(),
    install_requires=get_install_requires(),
    entry_points={
        "console_scripts": [
            "ecd=ecd:main"
        ],
    },
    # package_data={'ecd': [r'css/*', 'js/*', 'templates/*']},
    zip_safe=False,
    python_requires='>=3.0',
)
if __name__ == '__main__':
    import sys

    sys.argv = ['setup.py', 'sdist']
