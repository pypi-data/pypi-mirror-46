
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='notebookAutomationUtils', 
    version="1.0.2", 
    description='Tools for a notebook generator',  
    long_description=long_description,  
    long_description_content_type='text/markdown', 
    url='https://git.soma.salesforce.com/j-gao/notebook_automation_utils',  
    author='Tejal Parulekar, Jesse Gao', 
    author_email='tparulekar@salesforce.com, j.gao@salesforce.com', 
    packages=find_packages(),
    license='Private',
    classifiers=[  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='jupyter tools',  
    install_requires=[
        'setuptools >= 1.1.6'
    ],
    setup_requires=["pytest-runner"],
    tests_require=[
        'pytest'
    ],

    extras_require={  
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
