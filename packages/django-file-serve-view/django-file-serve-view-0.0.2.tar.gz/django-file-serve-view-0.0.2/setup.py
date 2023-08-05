# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-file-serve-view',
    version='0.0.2',
    author=u'Jon Combe',
    author_email='pypi@joncombe.net',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    url='https://github.com/joncombe/django-file-serve-view',
    license='BSD licence, see LICENCE file',
    description='Tiny file-serving class-based view (CBV) for Django',
    long_description='Tiny file-serving class-based view (CBV) for Django',
    zip_safe=False,
)
