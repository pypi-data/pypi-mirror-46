# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='tfthrift',
    version='0.0.1.beta',
    description='tfthrift',
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
    packages=['tflask', 'thrift_protocol'],
)