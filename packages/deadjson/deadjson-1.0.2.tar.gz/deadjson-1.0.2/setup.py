from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='deadjson',
    version='1.0.2',
    description='A Python library implementing a dict-like object that writes to a JSON file as it is modified',
    url='https://github.com/adityanugraha98/deadjson',
    packages= ["deadjson"],
    author='ADITYA NUGRAHA',
    author_email='adityana987@gmail.com',
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    py_modules=["deadjson"],
    project_urls={
        'Bug Reports': 'https://github.com/adityanugraha98/deadjson/issues',
    },
)