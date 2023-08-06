# -*- coding: utf-8 -*-
# python lib_setup.py sdist bdist_wheel upload
import os

from setuptools import setup

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


dir_path = os.path.dirname(os.path.realpath(__file__))


setup(
    name='thefiarlib',
    version='0.0.3.beta',
    description='thefiarlib',
    author='tf',
    author_email='tf@thefair.net.cn',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        '../library'
    ],
    install_requires=load_requirements(os.path.join(dir_path, '../requirements.txt'))
)
