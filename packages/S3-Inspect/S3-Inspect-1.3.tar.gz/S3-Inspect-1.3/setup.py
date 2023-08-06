# Work around mbcs bug in distutils. 
# http://bugs.python.org/issue10945
import codecs 
try: 
    codecs.lookup('mbcs') 
except LookupError: 
    ascii = codecs.lookup('ascii') 
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs') 
    codecs.register(func) 

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='S3-Inspect',
    version='1.3',
    description='A package to inspect contents of S3 buckets and generate report',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Syed Humair',
    author_email="syed.humair@gmail.com",
    keywords=['aws', 's3', 'challenge'],
    packages=['s3inspect', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    url='https://github.com/syedhumair/aws-devops-challenge',
    install_requires=requirements,
)
