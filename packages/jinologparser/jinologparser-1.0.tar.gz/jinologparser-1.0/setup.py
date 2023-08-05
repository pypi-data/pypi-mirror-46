from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='jinologparser',
    version='1.0',
    test_suite='log_test',
	author='Aleksandr Galanin',
	author_email='aleksandr.galanin@inbox.ru',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    url='http://example.com'
)