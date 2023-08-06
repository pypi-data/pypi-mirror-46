# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from django_cloud_essentials import __version__

PACKAGE = "django-cloud-essentials"

setup(
    name=PACKAGE,
    version=__version__,
    description='An opinionated django setup for Divio Cloud',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://www.divio.com',
    packages=find_packages(),
    package_dir={PACKAGE: PACKAGE},
    package_data={PACKAGE: ['addon.yml']},
    install_requires=(
        'Django',
        'django-getenv',
    ),
    include_package_data=True,
    zip_safe=False,
)
