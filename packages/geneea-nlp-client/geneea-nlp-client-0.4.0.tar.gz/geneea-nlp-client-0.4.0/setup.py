
from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='geneea-nlp-client',
    version='0.4.0',

    author='Geneea Analytics s.r.o',
    author_email='support@geneea.com',
    description='The SDK library and command-line interface to Geneea NLP REST API calls.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='geneea python nlp api cli',
    url='https://geneea.com',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License'
    ],

    # Dependencies
    install_requires=['requests~=2.21', 'retrying~=1.3'],
    dependency_links=[],
    extras_require={
        'examples':  ['pandas>=0.22']
    },


    packages=find_packages(),

    test_suite='tests'
)
