# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_flavour import __version__

PACKAGE = "django-flavour"

setup(
    name=PACKAGE,
    version=__version__,
    description="Adds flavour support for other django addons",
    author="Divio AG",
    author_email="info@divio.ch",
    url="https://www.divio.com",
    packages=find_packages(),
    package_dir={PACKAGE: PACKAGE},
    package_data={PACKAGE: ['addon.yml']},
    install_requires=("Django", "django-getenv", "libflavour", "strictyaml"),
    include_package_data=True,
    zip_safe=False,
)
