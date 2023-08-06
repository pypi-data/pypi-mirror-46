from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

long_description = ''
if path.isfile('README.md'):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

requirements = ['requests']

setup(
    name='python_riot',
    version='0.1.3',
    description='inoffical python lib for the Riot API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='riot riot-api leagueoflegends python lib',
    author='Johannes Eimer Production (JEP)',
    author_email='info@jep-dev.com',
    license='MIT',
    url='https://github.com/FourZeroOne/python_riot',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    python_requires='>=3.6'
)