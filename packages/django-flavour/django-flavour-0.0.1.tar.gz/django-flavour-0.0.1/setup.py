# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_flavour import __version__


setup(
    name="django-flavour",
    version=__version__,
    description='Adds flavour support for other django addons',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://www.divio.com',
    packages=find_packages(),
    install_requires=(
        'Django',
        'django-getenv',
    ),
    include_package_data=True,
    zip_safe=False,
)
