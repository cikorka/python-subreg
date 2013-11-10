# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='python-subreg',
    version='0.0.4',
    description='Python wrapper around the subreg.cz SOAP API',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='subreg subreg.cz',
    url='http://github.com/cikorka/python-subreg',
    author='Petr Jerabek',
    author_email='cikorka@me.com',
    license='MIT',
    packages=['subreg'],
    install_requires=[
        'SOAPpy',
    ],
    include_package_data=True,
    zip_safe=False,
)
