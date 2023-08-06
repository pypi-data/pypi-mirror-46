#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='unithon',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/dvidgar/unithon',
    download_url='https://github.com/dvidgar/unithon/archive/0.0.1.tar.gz',
    license='Apache License 2.0',
    author='David Garcia',
    author_email='dvid@usal.es',
    description='unithon - Python library to unify datasets',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['pandas==0.24.2',
                      'pytest==4.5'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    keywords='unithon, datasets, unification, data-science'
)
