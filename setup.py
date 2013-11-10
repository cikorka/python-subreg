# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='python-subreg',
    version='0.0.3',
    description='Python wrapper around the subreg.cz SOAP API',
    url='http://github.com/cikorka/python-subreg',
    author='cikorka',
    author_email='cikorka@me.com',
    license='MIT',
    packages=['subreg'],
    install_requires=[
        'SOAPpy',
    ],
    zip_safe=False
)
